import numpy as np

USER_PREF = [
    [(0 ,1), (1, 22), (2, 1), (3, 1), (5, 0)],
    [(0, 1), (1, 32), (2, 0), (3, 0), (4, 1), (5, 0)],
    [(0, 0), (1, 18), (2, 1), (3, 1), (4, 0), (5, 1)],
    [(0, 1), (1, 40), (2, 1), (3, 0), (4, 0), (5, 1)],
    [(0, 0), (1, 40), (2, 0), (4, 1), (5, 0)],
    [(0, 0), (1, 25), (2, 1), (3, 1), (4, 1)],
]

N_LATENT = 3
LAMBDA = 0.03
ITERATIONS = 20

def main():
    """ Run the iterations to find a local minimum in the "PCA"
    approach to recommender systems"""

    user_dict, item_dict = make_user_and_item_dict(USER_PREF)

    users = sorted(user_dict.keys())
    n_users = len(users)

    items = sorted(item_dict.keys())
    n_items = len(item_dict)

    print('Number of Users: %d' % n_users)
    print('Number of Items: %d' % n_items)

    V = np.random.rand(n_items, N_LATENT).astype(np.float32)

    for i in range(ITERATIONS):

        U = optimize_other(users, user_dict, V)
        V = optimize_other(items, item_dict, U)

        print('Error on iteration %d: %.2f' % (i, compute_error(U, V, user_dict)))

    print(U.dot(V.T))


def make_user_and_item_dict(user_pref_list):

    user_dict = dict()
    item_dict = dict()

    for user, user_pref in enumerate(user_pref_list):
        user_dict[user] = {item: value for item, value in user_pref}

    for user, user_pref in user_dict.items():
        for item, value in user_pref.items():
            if item in item_dict:
                item_dict[item][user] = value
            else:
                item_dict[item] = {user: value}

    return user_dict, item_dict

def optimize_other(sorted_keys, a_dict, other_matrix):

    keys = sorted_keys

    return_matrix = []
    for k in keys:
        prefs = a_dict[k]
        sub_matrix = []
        sub_prefs = []
        other_keys = sorted(prefs.keys())
        for other_key in other_keys:
            value = prefs[other_key]
            sub_matrix.append(other_matrix[other_key, :])
            sub_prefs.append(value)

        sub_matrix = np.array(sub_matrix, dtype=np.float32)
        sub_prefs = np.array(sub_prefs, dtype=np.float32)

        this_row = np.linalg.inv(
            sub_matrix.T.dot(sub_matrix) + LAMBDA* np.eye(N_LATENT)
        ).dot(sub_matrix.T).dot(sub_prefs)

        return_matrix.append(this_row)

    return np.array(return_matrix, dtype=np.float32)

def compute_error(U, V, user_dict):
    prediction = U.dot(V.T)

    error = 0.0
    for user, user_pref in user_dict.items():
        for item, pref in user_pref.items():
            error += (prediction[user, item] - pref) ** 2

    return(error)






if __name__ == '__main__':
    main()
