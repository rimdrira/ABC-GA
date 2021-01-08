from numpy import dot, array

#+----------------------------------------------------------------------------------------------+#


# fitness evaluation

def fit(cp, minQos, maxQos, weights):
    qos = cp.cpQos()
    rt = (maxQos['responseTime'] - qos['responseTime']) / (maxQos['responseTime'] - minQos['responseTime'])
    pr = (maxQos['price'] - qos['price']) / (maxQos['price'] - minQos['price'])
    av = (qos['availability'] - minQos['availability']) / (maxQos['availability'] - minQos['availability'])
    rel = (qos['reliability'] - minQos['reliability']) / (maxQos['reliability'] - minQos['reliability'])
    # vectorial product
    return dot(array([rt, pr, av, rel]), weights)
