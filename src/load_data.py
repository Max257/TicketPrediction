
def load_data(dataset, routes):
   
    isOneOptimalState = False
    # Construct the input data
    dim = routes.__len__() + 4
    X_train = np.empty(shape=(0, dim))
    y_train = np.empty(shape=(0,1))
    y_train_price = np.empty(shape=(0,1))
    X_test = np.empty(shape=(0,dim))
    y_test = np.empty(shape=(0,1))
    y_test_price = np.empty(shape=(0,1))

    for filePrefix in routes:
        datas = load_data_with_prefix_and_dataset(filePrefix, dataset)
        for data in datas:
            print "Construct route {}, State {}, departureDate {}...".format(filePrefix, data["State"], data["Date"])
            x_i = []
            # feature 1: flight number -> dummy variables
            for i in range(len(routes)):
                """
                !!!need to change!
                """
                if i == routes.index(filePrefix):
                    x_i.append(1)
                else:
                    x_i.append(0)

            # feature 2: departure date interval from "20151109", because the first observed date is 20151109
            departureDate = data["Date"]
            """
            !!!maybe need to change the first observed date
            """
            departureDateGap = util.days_between(departureDate, "20151109")
            x_i.append(departureDateGap)

            # feature 3: observed days before departure date
            state = data["State"]
            x_i.append(state)

            # feature 4: minimum price before the observed date
            minimumPreviousPrice = getMinimumPreviousPrice(data["Date"], state, datas)
            x_i.append(minimumPreviousPrice)

            # feature 5: maximum price before the observed date
            maximumPreviousPrice = getMaximumPreviousPrice(data["Date"], state, datas)
            x_i.append(maximumPreviousPrice)

            # output
            y_i = [0]
            specificDatas = []
            specificDatas = [data2 for data2 in datas if data2["Date"]==departureDate]

           

            #Method 2: multiple entries can be buy
            minPrice = getMinimumPrice(specificDatas)
            if util.getPrice(data["MinimumPrice"]) == minPrice:
                y_i = [1]


            # keep price info
            y_price = [util.getPrice(data["MinimumPrice"])]

            if int(departureDate) < 20160229 and int(departureDate) >= 20151129: # choose date between "20151129-20160229(20160115)" as training data
                X_train = np.concatenate((X_train, [x_i]), axis=0)
                y_train = np.concatenate((y_train, [y_i]), axis=0)
                y_train_price = np.concatenate((y_train_price, [y_price]), axis=0)
            elif int(departureDate) < 20160508 and int(departureDate) >= 20160229: # choose date before "20160508(20160220)" as test data
                X_test = np.concatenate((X_test, [x_i]), axis=0)
                y_test = np.concatenate((y_test, [y_i]), axis=0)
                y_test_price = np.concatenate((y_test_price, [y_price]), axis=0)
            else:
                pass

            # X_train = np.concatenate((X_train, [x_i]), axis=0)
            # y_train = np.concatenate((y_train, [y_i]), axis=0)
            # y_train_price = np.concatenate((y_train_price, [y_price]), axis=0)

        # end of for datas
    # end of for routes


    
    return X_train, y_train, X_test, y_test
