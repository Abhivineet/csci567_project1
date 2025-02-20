import numpy as np
from knn import KNN

############################################################################
# DO NOT MODIFY CODES ABOVE 
############################################################################


# TODO: implement F1 score
def f1_score(real_labels, predicted_labels):
    """
    Information on F1 score - https://en.wikipedia.org/wiki/F1_score
    :param real_labels: List[int]
    :param predicted_labels: List[int]
    :return: float
    """
    assert len(real_labels) == len(predicted_labels)
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for i in range(len(real_labels)):
        if predicted_labels[i] == 1:
            if real_labels[i] == 1:
                tp+=1
            else:
                fp+=1
        else:
            if real_labels[i] == 0:
                tn += 1
            else:
                fn+=1
    return ((tp*1.0)/(tp+((1/2.0)*(fp+fn))))
    # raise NotImplementedError


class Distances:
    @staticmethod
    # TODO
    def minkowski_distance(point1, point2):
        """
        Minkowski distance is the generalized version of Euclidean Distance
        It is also know as L-p norm (where p>=1) that you have studied in class
        For our assignment we need to take p=3
        Information on Minkowski distance - https://en.wikipedia.org/wiki/Minkowski_distance
        :param point1: List[float]
        :param point2: List[float]
        :return: float
        """
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)
        sub = abs(np.subtract(point1, point2))
        sub = sub**3
        out = np.cbrt(np.sum(sub))
        return out
        # raise NotImplementedError

    @staticmethod
    # TODO
    def euclidean_distance(point1, point2):
        """
        :param point1: List[float]
        :param point2: List[float]
        :return: float
        """
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)
        return np.linalg.norm(np.subtract(point1, point2), 2)
        # raise NotImplementedError

    @staticmethod
    # TODO
    def cosine_similarity_distance(point1, point2):
        """
       :param point1: List[float]
       :param point2: List[float]
       :return: float
       """
        point1 = np.asarray(point1)
        point2 = np.asarray(point2)
        l2_1 = np.linalg.norm(point1, 2)
        l2_2 = np.linalg.norm(point2, 2)
        if l2_1==0 or l2_2==0:
            return 1
        else:
            n = np.sum(point1*point2)
            return (1- (n/(l2_1*l2_2)))
        # raise NotImplementedError



class HyperparameterTuner:
    def __init__(self):
        self.best_k = None
        self.best_distance_function = None
        self.best_scaler = None
        self.best_model = None

    # TODO: find parameters with the best f1 score on validation dataset
    def tuning_without_scaling(self, distance_funcs, x_train, y_train, x_val, y_val):
        """
        In this part, you need to try different distance functions you implemented in part 1.1 and different values of k (among 1, 3, 5, ... , 29), and find the best model with the highest f1-score on the given validation set.
		
        :param distance_funcs: dictionary of distance functions (key is the function name, value is the function) you need to try to calculate the distance. Make sure you loop over all distance functions for each k value.
        :param x_train: List[List[int]] training data set to train your KNN model
        :param y_train: List[int] training labels to train your KNN model
        :param x_val:  List[List[int]] validation data
        :param y_val: List[int] validation labels

        Find the best k, distance_function (its name), and model (an instance of KNN) and assign them to self.best_k,
        self.best_distance_function, and self.best_model respectively.
        NOTE: self.best_scaler will be None.

        NOTE: When there is a tie, choose the model based on the following priorities:
        First check the distance function:  euclidean > Minkowski > cosine_dist 
		(this will also be the insertion order in "distance_funcs", to make things easier).
        For the same distance function, further break tie by prioritizing a smaller k.
        """
        
        # You need to assign the final values to these variables
        best_k = None
        best_distance_function = None
        best_model = None
        last_best_f1 = -1
        for key in distance_funcs:
            for k in range(1,30,2):
                model = KNN(k, distance_funcs[key])
                model.train(x_train, y_train)
                predictions = model.predict(x_val)
                f1 = f1_score(y_val, predictions)
                if f1>last_best_f1:
                    best_k = k
                    best_distance_function = key
                    best_model = model
                    last_best_f1=f1

        self.best_k = best_k
        self.best_distance_function = best_distance_function
        self.best_model = best_model
        # raise NotImplementedError

    # TODO: find parameters with the best f1 score on validation dataset, with normalized data
    def tuning_with_scaling(self, distance_funcs, scaling_classes, x_train, y_train, x_val, y_val):
        """
        This part is the same as "tuning_without_scaling", except that you also need to try two different scalers implemented in Part 1.3. More specifically, before passing the training and validation data to KNN model, apply the scalers in scaling_classes to both of them. 
		
        :param distance_funcs: dictionary of distance functions (key is the function name, value is the function) you need to try to calculate the distance. Make sure you loop over all distance functions for each k value.
        :param scaling_classes: dictionary of scalers (key is the scaler name, value is the scaler class) you need to try to normalize your data
        :param x_train: List[List[int]] training data set to train your KNN model
        :param y_train: List[int] train labels to train your KNN model
        :param x_val: List[List[int]] validation data
        :param y_val: List[int] validation labels

        Find the best k, distance_function (its name), scaler (its name), and model (an instance of KNN), and assign them to self.best_k, self.best_distance_function, best_scaler, and self.best_model respectively.
        
        NOTE: When there is a tie, choose the model based on the following priorities:
        First check scaler, prioritizing "min_max_scale" over "normalize" (which will also be the insertion order of scaling_classes). Then follow the same rule as in "tuning_without_scaling".
        """
        
        # You need to assign the final values to these variables
        best_k = None
        best_distance_function = None
        best_scaler = None
        best_model = None
        last_best_f1 = -1
        for scale in scaling_classes:
            scaler = scaling_classes[scale]()
            scaled_x_train = scaler(x_train)
            scaled_x_val = scaler(x_val)
            for func in distance_funcs:
                for k in range(1,min(30,len(y_train)+1),2):
                    model = KNN(k, distance_funcs[func])
                    model.train(scaled_x_train,y_train)
                    predictions = model.predict(scaled_x_val)
                    f1 = f1_score(y_val, predictions)
                    if f1 > last_best_f1:
                        best_k = k
                        best_distance_function = func
                        best_model = model
                        best_scaler = scale
                        last_best_f1 = f1

        self.best_k = best_k
        self.best_distance_function = best_distance_function
        self.best_scaler = best_scaler
        self.best_model = best_model

        # raise NotImplementedError


class NormalizationScaler:
    def __init__(self):
        pass

    # TODO: normalize data
    def __call__(self, features):
        """
        Normalize features for every sample

        Example
        features = [[3, 4], [1, -1], [0, 0]]
        return [[0.6, 0.8], [0.707107, -0.707107], [0, 0]]

        :param features: List[List[float]]
        :return: List[List[float]]
        """
        out = list()
        for feature in features:
            feature = np.asarray(feature)
            l2_feature = np.linalg.norm(feature, 2)
            if l2_feature==0:
                out.append(feature)
            else:
                out.append(feature/l2_feature)
        return out
        # raise NotImplementedError

class MinMaxScaler:
    def __init__(self):
        pass

    # TODO: min-max normalize data
    def __call__(self, features):
        """
		For each feature, normalize it linearly so that its value is between 0 and 1 across all samples.
        For example, if the input features are [[2, -1], [-1, 5], [0, 0]],
        the output should be [[1, 0], [0, 1], [0.333333, 0.16667]].
		This is because: take the first feature for example, which has values 2, -1, and 0 across the three samples.
		The minimum value of this feature is thus min=-1, while the maximum value is max=2.
		So the new feature value for each sample can be computed by: new_value = (old_value - min)/(max-min),
		leading to 1, 0, and 0.333333.
		If max happens to be same as min, set all new values to be zero for this feature.
		(For further reference, see https://en.wikipedia.org/wiki/Feature_scaling.)

        :param features: List[List[float]]
        :return: List[List[float]]
        """
        features = np.asarray(features, dtype='float')
        for i in range(len(features[0])):
            den = features[:,i].max() - features[:,i].min()
            if den ==0:
                features[:,i] = np.zeros(np.shape(features[:,i]))
            else:
                features[:,i] = (features[:,i] - features[:,i].min())/(den)
        return features

        # raise NotImplementedError
