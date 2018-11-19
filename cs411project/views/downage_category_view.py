from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
import numpy as np

from ..database.entity_serializer import EntitySerializer
from ..database.constants import PREBAKED_DOWNAGE_CATEGORY_TEXTS
from ..nlp.preprocess_corpus import Preprocessing
from ..nlp.downage_categories import DownageCategories

import json

class SimpleDownageCategoryStartBatchView(MethodView):

    # The maximum amount of comments to use for determining downage categories
    MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH = 100 

    # Number of downage categories to choose for each batch (or for each machine in each batch
    #   if doing per-machine downage categories)
    NUM_DOWNAGE_CATEGORIES = 5

    MU = 0.001

    def post(self):
        
        """Start a batch job to compute and store downage categories in a simple way

           Compute downage categories by computing the probabilities of each token 
               among the most recent MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH comments updated
               across the entire lab, and then selecting the top NUM_DOWNAGE_CATEGORIES
               tokens as the downage categories
        """
        connection  = g.mysql_connection.get_connection()
        cursor = connection.cursor(prepared=True)
        # Persist to DB that we are starting a new batch
        new_batch_query = "INSERT INTO DownageCategoryBatch(BatchID) VALUES (NULL)";
        cursor.execute(new_batch_query)
        batch_id = cursor.lastrowid


        get_comments_query = "SELECT * FROM Comments ORDER BY LastModifiedTS DESC LIMIT %s"
        cursor.execute(get_comments_query, (SimpleDownageCategoryStartBatchView.MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH,))
        col_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))




        # Perform some preprocessing on the corpus
        comment_corpus = [comment['CommentText'] for comment in result_as_dicts]
        _, id2token, corpus_bow = Preprocessing.preprocess_corpus(comment_corpus)

        # Compute downage categories on a per-lab level as well (in case some machines don't have comments
        #    yet...those machines can use per-lab downage categories as a fallback)
        tokens, word_probs = DownageCategories.calculate_word_probabilities(corpus_bow, id2token, SimpleDownageCategoryStartBatchView.MU)
        sorted_tokens, sorted_word_probs = DownageCategories.sort_tokens_by_probability(tokens, word_probs)
        lab_wide_downage_categories_tokens = sorted_tokens[:SimpleDownageCategoryStartBatchView.NUM_DOWNAGE_CATEGORIES]

        # Persist lab-wide results to DB, using a NULL MachineID to indicate lab-wide downage categories
        lab_wide_downage_insert_query = """
           INSERT INTO DownageCategory(BatchID, BatchRank, CategoryText, MachineID)
               VALUES (%s, %s, %s, NULL)
        """

        for idx, token in enumerate(lab_wide_downage_categories_tokens):
            batch_rank = idx + 1
            cursor.execute(lab_wide_downage_insert_query, (batch_id, batch_rank, token))


        # Close transaction
        connection.commit()
        cursor.close()
        return jsonify("Success")


class SimpleDownageCategoryView(MethodView):

    def get(self):
        """Get the lab-wide downage categories
        """
        connection  = g.mysql_connection.get_connection()

        result_as_dicts = SimpleDownageCategoryView.get_simple_downage_categories(connection)

        connection.commit()
        return jsonify(result_as_dicts)

    @classmethod
    def get_simple_downage_categories(cls, connection):
        """Get the 'simple' downage categories from the DB

           Caller must call .commit() on the connection
        """
        cursor = connection.cursor(prepared=True)

        get_latest_batch_id_query = """
           SELECT BatchID
           FROM DownageCategoryBatch
           WHERE CompletedTS = (SELECT MAX(CompletedTS) FROM DownageCategoryBatch)
        """

        cursor.execute(get_latest_batch_id_query)
        batch_id = int(cursor.fetchone()[0])

        get_latest_downage_categories_query = """
           SELECT * FROM DownageCategory WHERE BatchID = (%s) AND MachineID IS NULL
        """

        cursor.execute(get_latest_downage_categories_query, (batch_id,))
        col_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))

        cursor.close()

        return result_as_dicts



class MixtureModelDownageCategoryStartBatchView(MethodView):

    # The maximum amount of comments to use for determining downage categories
    MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH = 100 

    # Number of downage categories to choose for each batch (or for each machine in each batch
    #   if doing per-machine downage categories)
    NUM_DOWNAGE_CATEGORIES = 5

    ALPHA = 0.55

    MU = 0.0001


    def post(self):
        """Start a batch job to compute the downage categories using a simple mixture model

           This endpoint also computes the downage categories in the same way as SimpleDownageCategoryStartBatchView,
               persisting them under the same BatchID as the mixture model downage categories
               with MachineID set to NULL

           Grabs the MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH most recently updated comments
               across the lab as our input corpus, then splits that input corpus into
               comments made for machine M vs all other comments...for every machine M
               that has at least one comment in the input corpus

           If there are no comments for a given machine M within the input corpus,
               then no downage categories are computed for that machine. Retrieving
               the downage categories for M will resort to falling back to the
               "simple" downage categories as they are computed in SimpleDownageCategoryStartBatchView

           See nlp.determine_downage_categories() for an explanation on how downage categories
               are computed
        """
        connection  = g.mysql_connection.get_connection()
        cursor = connection.cursor(prepared=True)


        # Persist to DB that we are starting a new batch
        new_batch_query = "INSERT INTO DownageCategoryBatch(BatchID) VALUES (NULL)";
        cursor.execute(new_batch_query)
        batch_id = cursor.lastrowid


        # Get all the Comments we want to use for the batch
        get_comments_query = "SELECT * FROM Comments ORDER BY LastModifiedTS DESC LIMIT %s"
        cursor.execute(get_comments_query, (MixtureModelDownageCategoryStartBatchView.MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH,))
        col_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))


        # Compute downage categories on a per-machine level
        comment_corpus = [comment['CommentText'] for comment in result_as_dicts]
        machine_of_comments = [comment['MachineID'] for comment in result_as_dicts]
        sorted_machine_ids = np.unique(machine_of_comments)
        _, id2token, corpus_bow = Preprocessing.preprocess_corpus(comment_corpus)

        machine_downage_categories = DownageCategories.determine_downage_categories(
            corpus_bow,
            machine_of_comments,
            id2token,
            MixtureModelDownageCategoryStartBatchView.NUM_DOWNAGE_CATEGORIES,
            MixtureModelDownageCategoryStartBatchView.ALPHA,
            MixtureModelDownageCategoryStartBatchView.MU
        )

        # Persist per-machine results to DB
        per_machine_downage_insert_query = """
           INSERT INTO DownageCategory(BatchID, BatchRank, CategoryText, MachineID) 
               VALUES (%s, %s, %s, %s)
        """
        for idx, x in enumerate(machine_downage_categories):
            sorted_tokens = x[0]
            machine_id = int(sorted_machine_ids[idx])

            for token_idx, token in enumerate(sorted_tokens):
                batch_rank = token_idx + 1
                cursor.execute(per_machine_downage_insert_query, (batch_id, batch_rank, token, machine_id))



        # Compute downage categories on a per-lab level as well (in case some machines don't have comments
        #    yet...those machines can use per-lab downage categories as a fallback)
        tokens, word_probs = DownageCategories.calculate_word_probabilities(corpus_bow, id2token, MixtureModelDownageCategoryStartBatchView.MU)
        sorted_tokens, sorted_word_probs = DownageCategories.sort_tokens_by_probability(tokens, word_probs)
        lab_wide_downage_categories_tokens = sorted_tokens[:MixtureModelDownageCategoryStartBatchView.NUM_DOWNAGE_CATEGORIES]


        # Persist lab-wide results to DB, using a NULL MachineID to indicate lab-wide downage categories
        lab_wide_downage_insert_query = """
           INSERT INTO DownageCategory(BatchID, BatchRank, CategoryText, MachineID)
               VALUES (%s, %s, %s, NULL)
        """

        for idx, token in enumerate(lab_wide_downage_categories_tokens):
            batch_rank = idx + 1
            cursor.execute(lab_wide_downage_insert_query, (batch_id, batch_rank, token))


        # Close transaction
        connection.commit()
        cursor.close()
        return jsonify("Success")


class MixtureModelDownageCategoryView(MethodView):

    def get(self, machine_id):

        """Get the downage categories for machine machine_id from the most recently persisted downage category batch

           Note that if there were no downage categories computed for the machine with id machine_id
               (non-existent machine_id, or the specified machine had 0 comments in the input corpus
               for MixtureModelDownageCategoryStartBatchView), then this endpoint will return
               the "simple" downage categories as specified in SimpleDownageCategoryStartBatchView
        """

        connection  = g.mysql_connection.get_connection()

        result_as_dicts = MixtureModelDownageCategoryView.get_downage_categories_for_machine(connection, machine_id)

        connection.commit()
        return jsonify(result_as_dicts)

    @classmethod
    def get_downage_categories_for_machine(cls, connection, machine_id):
        """Get the downage categories for a given machine, falling back to lab-wide 'simple' downage categories if needed

            Caller must call .commit() on the connection
        """

        cursor = connection.cursor(prepared=True)

        # Get latest batch id
        get_latest_batch_id_query = """
           SELECT BatchID
           FROM DownageCategoryBatch
           WHERE CompletedTS = (SELECT MAX(CompletedTS) FROM DownageCategoryBatch)
        """

        cursor.execute(get_latest_batch_id_query)
        batch_id = int(cursor.fetchone()[0])

        get_downage_categories_for_machine_query = """
           SELECT *
           FROM DownageCategory
           WHERE BatchID = %s AND MachineID = %s
        """
        cursor.execute(get_downage_categories_for_machine_query, (batch_id, machine_id))

        col_names = [x[0] for x in cursor.description]
        result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))

        # There are no downage categories for this machine, fall back to lab-wide downage categories
        if len(result_as_dicts) == 0:
            print("Falling back to downage categories that are lab-wide for same batch id")

            result_as_dicts = SimpleDownageCategoryView.get_simple_downage_categories(connection)

        cursor.close()

        return result_as_dicts


class DownageCategoriesEditingExistingCommentView(MethodView):

    def get(self, comment_id):
        """Returns the downage categories available for an existing comment

           The union of the following sets for comment C with id comment_id:
            * DownageCategories for the machine M that C is associated with
            * The prebaked downage categories
            * The existing category for C

           The results are returned in a list of JSON objects with 
            the schema of DownageCategory relation (with some fields
            set to NULL if we cannot determine them (e.g. BatchID for the prebaked downage categories))
        """
        connection = g.mysql_connection.get_connection()
        result_as_dicts = DownageCategoriesEditingExistingCommentView.get_downage_categories_for_editing_comment(connection, comment_id)
        connection.close()
        return jsonify(result_as_dicts)

    @classmethod
    def get_downage_categories_for_editing_comment(cls, connection, comment_id):
        """Get the downage categories needed for editing a comment
        """
        
        cursor = connection.cursor(prepared=True)

        
        get_machine_id_of_comment_query = """
            SELECT MachineID, Category FROM Comments WHERE CommentID = %s
        """
        cursor.execute(get_machine_id_of_comment_query, (comment_id,))
        row = cursor.fetchone()
        machine_id = int(row[0])
        existing_comment_category = row[1]
        computed_downage_categories_dicts = MixtureModelDownageCategoryView.get_downage_categories_for_machine(connection, machine_id)


        scalar_downage_categories = [x for x in PREBAKED_DOWNAGE_CATEGORY_TEXTS]
        scalar_downage_categories.append(existing_comment_category)

        # Combine the downage category of comment C, the prebaked downage categories, and downage categories for machine M
        #   s.t. each element in the resulting list is a dictionary with the same keys, but None for any values
        #   that cannot be inferred from the scalar category texts of C's existing downage category and the prebaked 
        #   downage categories
        result_as_dicts = [x for x in computed_downage_categories_dicts]
        for category_text in scalar_downage_categories:
            # Keys taken from DDL for DownageCategory
            result_as_dicts.append({
                'DownageCategoryID': None,
                'BatchID': None,
                'BatchRank': None,
                'CategoryText': category_text,
                'MachineID': None
            })

        return result_as_dicts


        
        

        


