from tkinter import *
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

X = None
y = None


def process_data(data):
    cols_rating = ["user_id", "item_id", "rating"]
    data_processed = pd.DataFrame(data, columns=cols_rating).sort_values(
        by=["user_id", "item_id"]
    )

    global X
    X = data_processed["user_id"].unique()
    global y
    y = data_processed["item_id"].unique()
    return data_processed


def predict_matrix(normalize_matrix, similarity_matrix, K):
    num_users, num_items = normalize_matrix.shape
    pred_matrix = np.zeros((num_users, num_items))

    for item_idx in range(num_items):
        rated_users = np.nonzero(normalize_matrix[:, item_idx])[
            0
        ]  # Danh sách các users đã rated cho item_idx

        for user_idx in range(num_users):
            if (
                normalize_matrix[user_idx, item_idx] == 0
            ):  # Nếu user_idx chưa rated cho item_idx
                similarity_values = similarity_matrix[
                    user_idx, rated_users
                ]  # Giá trị similarities của user_idx với các users đã rated
                top_K_indices = np.argsort(-similarity_values)[
                    :K
                ]  # Chọn K giá trị lớn nhất
                top_K_values = similarity_values[
                    top_K_indices
                ]  # Giá trị similarities của K users có similarities lớn nhất
                normalized_ratings = normalize_matrix[
                    rated_users[top_K_indices], item_idx
                ]  # Ratings normalized của K users

                # Tính pred rating cho user_idx và item_idx
                pred_rating = np.dot(top_K_values, normalized_ratings) / np.sum(
                    np.abs(top_K_values)
                )
                pred_matrix[user_idx, item_idx] = pred_rating

    return pred_matrix


def get_recommendations(user_id, pred_matrix, ratings_matrix, item_titles):
    # Xác định các sản phẩm chưa được user_id đánh giá (có giá trị NaN)
    unrated_items_indices = np.where(np.isnan(ratings_matrix[user_id]))[0]
    # Tính toán pred ratings cho user_id cho các sản phẩm chưa đánh giá
    pred_ratings = pred_matrix[user_id, unrated_items_indices]
    # Sắp xếp danh sách các bộ giá trị rating
    sorted_indices = np.argsort(pred_ratings)[::-1]
    # Trả về các tiêu đề tương ứng với chỉ số của các phần tử trên cùng
    recommended_titles = [
        item_titles[item_idx] for item_idx in unrated_items_indices[sorted_indices]
    ]

    return recommended_titles


def RecommenderProduct(user_id, users, products, users_rated):
    data_ratings = process_data(users_rated)
    data_ratings["user_id"] = data_ratings["user_id"].map(users)
    data_ratings["item_id"] = data_ratings["item_id"].map(products)
    matrix_ratings = []
    X = data_ratings["user_id"].unique()
    y = data_ratings["item_id"].unique()
    for i in X:
        row = []
        for j in y:
            rating = data_ratings[
                (data_ratings["user_id"] == i) & (data_ratings["item_id"] == j)
            ]["rating"]
            if rating.empty:
                row.append(np.nan)
            else:
                row.append(float(rating.values[0]))
        matrix_ratings.append(row)

    matrix_ratings = np.array(matrix_ratings).T

    mean_users = np.nanmean(matrix_ratings, axis=0)

    normalize_matrix = np.empty_like(matrix_ratings)
    for i in range(matrix_ratings.shape[1]):
        user = matrix_ratings[:, i]
        mean_user = mean_users[i]
        normalize_matrix[:, i] = user - mean_user
    normalize_matrix[np.isnan(normalize_matrix)] = 0

    similarity_matrix = cosine_similarity(normalize_matrix.T)
    pred_matrix = predict_matrix(normalize_matrix.T, similarity_matrix, 2).T
    list_product_recommender = get_recommendations(
        users[user_id], pred_matrix.T, matrix_ratings.T, y
    )

    return list_product_recommender


def MainRS(data, user_id):

    users_rated = process_data(data)
    global X, y
    products = {}
    for index, i in enumerate(y):
        products[i] = index
    users = {}
    for index, i in enumerate(X):
        users[i] = index
    list_rs = RecommenderProduct(user_id, users, products, users_rated)
    rs = []
    for index_rs in list_rs:
        for key, value in products.items():
            if value == index_rs:
                rs.append(key)
    return rs


# data = [
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product6", 4],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product4", 2],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product8", 3],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product7", 1],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product5", 1],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product1", 3],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product3", 3],
#     ["9zwcdxfTaPT0PZzm84cFt6IUQb22", "product2", 4],
#     ["GBvBEpap5rNSQRjbVxBvl1yVaQM2", "product1", 5],
#     ["GBvBEpap5rNSQRjbVxBvl1yVaQM2", "product2", 4],
#     ["GBvBEpap5rNSQRjbVxBvl1yVaQM2", "product3", 2],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product6", 3],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product10", 4],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product4", 4],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product88", 2],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product5", 3],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product1", 4],
#     ["TZhjLTWTw2Mjpnjlu1rU1G1vQCp2", "product43", 1],
# ]