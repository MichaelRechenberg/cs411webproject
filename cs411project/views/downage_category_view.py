from flask import g, Flask, request
from flask.json import jsonify
from flask.views import MethodView
import numpy as np

from ..database.entity_serializer import EntitySerializer
from ..nlp.preprocess_corpus import Preprocessing
from ..nlp.downage_categories import DownageCategories

import json

# TODO: docstring
class SimpleDownageCategoryStartBatchView(MethodView):

    # The maximum amount of comments to use for determining downage categories
    MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH = 100 

    # Number of downage categories to choose for each batch (or for each machine in each batch
    #   if doing per-machine downage categories)
    NUM_DOWNAGE_CATEGORIES = 5

    MU = 0.001

    def post(self):
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

         # TODO: remove after debugging
         print("===")
         print(lab_wide_downage_categories_tokens)
         print("===")

         # Persist lab-wide results to DB
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
         connection  = g.mysql_connection.get_connection()
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

         connection.commit()
         cursor.close()
         return jsonify(result_as_dicts)



# TODO: docstring
class MixtureModelDownageCategoryStartBatchView(MethodView):

    # The maximum amount of comments to use for determining downage categories
    MAX_NUM_COMMENTS_FOR_DOWNAGE_BATCH = 100 

    # Number of downage categories to choose for each batch (or for each machine in each batch
    #   if doing per-machine downage categories)
    NUM_DOWNAGE_CATEGORIES = 5

    ALPHA = 0.55

    MU = 0.0001


    def post(self):
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


         # Persist lab-wide results to DB
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

         connection  = g.mysql_connection.get_connection()
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

             get_downage_categories_for_lab_query = """
                SELECT *
                FROM DownageCategory
                WHERE BatchID = %s AND MachineID IS NULL
             """
             cursor.execute(get_downage_categories_for_lab_query, (batch_id,))
             col_names = [x[0] for x in cursor.description]
             result_as_dicts = list(EntitySerializer.db_entities_to_python(cursor, col_names))


         connection.commit()
         cursor.close()
         return jsonify(result_as_dicts)

