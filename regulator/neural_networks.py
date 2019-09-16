class RotNetDataGenerator(Iterator):

    def __init__(self, input, batch_size=64,
                 preprocess_func=None, shuffle=False):

        self.images = input
        self.batch_size = batch_size
        self.input_shape = self.images.shape[1:]
        self.preprocess_func = preprocess_func
        self.shuffle = shuffle
        # add dimension if the images are greyscale
        if len(self.input_shape) == 2:
            self.input_shape = self.input_shape + (1,)
        N = self.images.shape[0]

        super(RotNetDataGenerator, self).__init__(N, batch_size, shuffle, None)

    def next(self):
        with self.lock:
            # get input data index and size of the current batch
            index_array, _, current_batch_size = next(self.index_generator)

        # create array to hold the images
        batch_x = np.zeros((current_batch_size,) + self.input_shape, dtype='float32')
        # create array to hold the labels
        batch_y = np.zeros(current_batch_size, dtype='float32')

        # iterate through the current batch
        for i, j in enumerate(index_array):
            image = self.images[j]

            # get a random angle
            rotation_angle = np.random.randint(360)

            # rotate the image
            rotated_image = rotate(image, rotation_angle)

            # add dimension to account for the channels if the image is greyscale
            if rotated_image.ndim == 2:
                rotated_image = np.expand_dims(rotated_image, axis=2)

            # store the image and label in their corresponding batches
            batch_x[i] = rotated_image
            batch_y[i] = rotation_angle

        # convert the numerical labels to binary labels
        batch_y = to_categorical(batch_y, 360)

        # preprocess input images
        if self.preprocess_func:
            batch_x = self.preprocess_func(batch_x)

        return batch_x, batch_y

# we don't need the labels indicating the digit value, so we only load the images
(X_train, _), (X_test, _) = mnist.load_data()

# number of convolutional filters to use
nb_filters = 64
# size of pooling area for max pooling
pool_size = (2, 2)
# convolution kernel size
kernel_size = (3, 3)

nb_train_samples, img_rows, img_cols, img_channels = X_train.shape
input_shape = (img_rows, img_cols, img_channels)
nb_test_samples = X_test.shape[0]

# model definition
input = Input(shape=(img_rows, img_cols, img_channels))
x = Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                  activation='relu')(input)
x = Convolution2D(nb_filters, kernel_size[0], kernel_size[1],
                  activation='relu')(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Dropout(0.25)(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.25)(x)
x = Dense(nb_classes, activation='softmax')(x)

model = Model(input=input, output=x)

# model compilation
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=[angle_error])

# training parameters
batch_size = 128
nb_epoch = 50

# callbacks
checkpointer = ModelCheckpoint(
    filepath=output_filename,
    save_best_only=True
)
early_stopping = EarlyStopping(patience=2)
tensorboard = TensorBoard()

# training loop
model.fit_generator(
    RotNetDataGenerator(
        X_train,
        batch_size=batch_size,
        preprocess_func=binarize_images,
        shuffle=True
    ),
    samples_per_epoch=nb_train_samples,
    nb_epoch=nb_epoch,
    validation_data=RotNetDataGenerator(
        X_test,
        batch_size=batch_size,
        preprocess_func=binarize_images
    ),
    nb_val_samples=nb_test_samples,
    verbose=1,
    callbacks=[checkpointer, early_stopping, tensorboard]
)

# randomly rotate an image
original_img = X_test[0]
true_angle = np.random.randint(360)
rotated_img = rotate(original_img, true_angle)
print('True angle: ', true_angle)

# add dimensions to account for the batch size and channels, 
rotated_img = rotated_img[np.newaxis, :, :, np.newaxis]
# convert to float
rotated_img = rotated_img.astype('float32')
# binarize image
rotated_img_bin = binarize_images(rotated_img)
# predict rotation angle
output = model.predict(rotated_img_bin)
predicted_angle = np.argmax(output)
print('Predicted angle: ', predicted_angle)
