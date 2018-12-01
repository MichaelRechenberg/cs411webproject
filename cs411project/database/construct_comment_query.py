# These keys match the column names in the DDL for comments
COMMENT_QUERY_KEY_MACHINE_ID = 'MachineID'
COMMENT_QUERY_KEY_AUTHOR_NETID = 'AuthorNetID'
COMMENT_QUERY_KEY_IS_RESOLVED = 'IsResolved'
COMMENT_QUERY_KEY_LAST_MODIFIED = 'LastModifiedTS'
COMMENT_QUERY_KEY_DOWNAGE_CATEGORY = 'Category'
COMMENT_QUERY_KEY_COMMENT_TEXT = 'CommentText'

# This key is just for signifying the sorting list
COMMENT_QUERY_KEY_SORT_LIST = 'SortingAttributes'

# Map a Comment column to the appropriate WHERE clause to AND with the rest of the query
WHERE_CLAUSE_PREPARED_STMT_DICT = {
    COMMENT_QUERY_KEY_MACHINE_ID: '{0} = (%s)'.format(COMMENT_QUERY_KEY_MACHINE_ID),
    COMMENT_QUERY_KEY_AUTHOR_NETID: '{0} = (%s)'.format(COMMENT_QUERY_KEY_AUTHOR_NETID),
    COMMENT_QUERY_KEY_IS_RESOLVED: '{0} = (%s)'.format(COMMENT_QUERY_KEY_IS_RESOLVED),
    # MySQL LIKE is case-insensitive by default
    COMMENT_QUERY_KEY_DOWNAGE_CATEGORY: "{0} LIKE (%s)".format(COMMENT_QUERY_KEY_DOWNAGE_CATEGORY),
    COMMENT_QUERY_KEY_COMMENT_TEXT: "{0} LIKE (%s)".format(COMMENT_QUERY_KEY_COMMENT_TEXT)
}

# Map a value for a Comment's column to the value passed into the prepared statement's parameter tuple
WHERE_CLAUSE_PARAM_CREATOR_DICT = {
    COMMENT_QUERY_KEY_MACHINE_ID: (lambda x: x),
    COMMENT_QUERY_KEY_AUTHOR_NETID: (lambda x: x),
    COMMENT_QUERY_KEY_IS_RESOLVED: (lambda x: x),
    # MySQL LIKE is case-insensitive by default
    COMMENT_QUERY_KEY_DOWNAGE_CATEGORY: (lambda x: "%{0}%".format(x)),
    COMMENT_QUERY_KEY_COMMENT_TEXT: (lambda x: "%{0}%".format(x)),
}

def construct_comment_select_query(query_dict):
    """Construct a prepared SELECT query to grab all the comments w.r.t. conditions
        specified in query_dict


        Params:
            query_dict: A dictionary containing various additional constraints
                to add to the select query. See below for valid keys. Conditions
                are AND'd together (e.g. if COMMENT_QUERY_KEY_MACHINE_ID and 
                COMMENT_QUERY_KEY_AUTHOR_NETID are present, then we return comments
                that were made by the user with netid COMMENT_QUERY_KEY_AUTHOR_NETID and
                were for machine COMMENT_QUERY_KEY_MACHINE_ID)


                Only values equal to COMMENT_QUERY_KEY* are accepted for WHERE and SORT BY clauses

                WHERE -> COMMENT_QUERY_KEY_MACHINE_ID, COMMENT_QUERY_KEY_IS_RESOLVED, COMMENT_QUERY_KEY_AUTHOR_NETID, 
                            COMMENT_QUERY_KEY_DOWNAGE_CATEGORY, COMMENT_QUERY_KEY_COMMENT_TEXT

                    Note that COMMENT_QUERY_KEY_MACHINE_ID, COMMENT_QUERY_KEY_IS_RESOLVED, and COMMENT_QUERY_KEY_AUTHOR_NETID use equality with = to filter comments. 

                    Note that COMMENT_QUERY_KEY_DOWNAGE_CATEGORY uses case-insensitive LIKE to filter comments

                SORT BY -> COMMENT_QUERY_KEY_LAST_MODIFIED, COMMENT_QUERY_KEY_IS_RESOLVED


            COMMENT_QUERY_KEY_MACHINE_ID: (value type string) If present, select only comments made for this machine
            COMMENT_QUERY_KEY_AUTHOR_NETID: (value type string) If present, select only comments made by the user with this netID
            COMMENT_QUERY_KEY_IS_RESOLVED: (value type int) If present, select only comments with this value for IsResolved
                (0 means unresolved, 1 means resolved)
            COMMENT_QUERY_KEY_COMMENT_TEXT: (value type string) If present, select only comments that contain this string as a substring
                of the comment text (case-insenstivit)
            COMMENT_QUERY_KEY_DOWNAGE_CATEGORY: (value type string) If present, select only comments that contain this string as a substring
                of the comment Category
            COMMENT_QUERY_KEY_SORT_LIST: (value type list) If present, sort the resulting comments by the attributes 
                present in this list. Multiple levels of sorting are supported


            For example, to get all the machines made by 'rchnbrg2' on machine 7, sorted by last modified timestamp, 
                query_dict would be:

                {
                    COMMENT_QUERY_KEY_MACHINE_ID: 7,
                    COMMENT_QUERY_KEY_AUTHOR_NETID: 'rchnbrg2',
                    COMMENT_QUERY_KEY_SORT_LIST: [COMMENT_QUERY_KEY_LAST_MODIFIED]
                }

        Returns:
            (prepared_stmt, args) where

            prepared_stmt -> The prepared statement of SQL
            args -> A tuple of arguments to populate the (%s) fields of the prepared_stmt
    """

    prepared_stmt = 'SELECT * FROM Comments' 

    where_attributes_set = set(query_dict.keys()).intersection(set(
        [
            COMMENT_QUERY_KEY_DOWNAGE_CATEGORY,
            COMMENT_QUERY_KEY_MACHINE_ID,
            COMMENT_QUERY_KEY_IS_RESOLVED,
            COMMENT_QUERY_KEY_AUTHOR_NETID,
            COMMENT_QUERY_KEY_COMMENT_TEXT
        ]
    ))

    prepared_stmt_args_list = []

    # Add WHERE clause if needed
    if len(where_attributes_set) > 0:

        # AND together as many WHERE clauses as needed
        prepared_stmt += ' WHERE ('
        where_attributes_list = list(where_attributes_set)
        prepared_stmt += ' AND '.join([WHERE_CLAUSE_PREPARED_STMT_DICT[attr] for attr in where_attributes_list])
        prepared_stmt += ')'

        
        # Construct the argument tuple for the prepared statement
        for attr in where_attributes_list:
            param_creator = WHERE_CLAUSE_PARAM_CREATOR_DICT[attr]
            param = param_creator(query_dict[attr])
            prepared_stmt_args_list.append(param)

    # Add SORT BY clause if needed
    if COMMENT_QUERY_KEY_SORT_LIST in query_dict:
        sort_by_attributes_set = set(query_dict[COMMENT_QUERY_KEY_SORT_LIST]).intersection(set([COMMENT_QUERY_KEY_IS_RESOLVED, COMMENT_QUERY_KEY_LAST_MODIFIED]))
        prepared_stmt += ' ORDER BY '
        prepared_stmt += ', '.join(list(sort_by_attributes_set))

    return (prepared_stmt, tuple(prepared_stmt_args_list))

