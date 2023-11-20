import tensorflow as tf
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.applications import EfficientNetB0
# Define a custom callback to print metrics after each epoch
class CustomCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        val_loss = logs.get('val_loss')
        val_accuracy = logs.get('val_accuracy')
        print(f"Epoch {epoch + 1}/{self.params['epochs']}: "
              f"loss: {logs['loss']:.4f}, accuracy: {logs['accuracy']:.4f}, "
              f"val_loss: {val_loss:.4f}, val_accuracy: {val_accuracy:.4f}")


# Set up data augmentation for training and validation data
train_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)


val_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.efficientnet.preprocess_input,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

# Adjust this path
data_directory = 'C:\\Users\\user\\Desktop\\firstModel\\modelData\\train'
train_generator = train_datagen.flow_from_directory(
    data_directory,  # Adjust the path
    target_size=(480, 480),
    batch_size=4,
    class_mode='binary',
)
data_directory = 'C:\\Users\\user\\Desktop\\firstModel\\modelData\\val'
validation_generator = val_datagen.flow_from_directory(
    data_directory,
    target_size=(480, 480),
    batch_size=4,
    class_mode='binary',
)

# Create the functional model
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(480, 480, 3))

# Unfreeze some top layers of the EfficientNetB0
# for layer in base_model.layers[-10:]:  # Unfreeze the top 10 layers
#     layer.trainable = True
for layer in base_model.layers:
    layer.trainable = False
for layer in base_model.layers[-10:]:
    layer.trainable=True
x = GlobalAveragePooling2D()(base_model.output)
x = Dense(128, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)

# Compile the model with a custom loss function that minimizes false positives
def custom_loss(y_true, y_pred):
    false_positives = tf.reduce_sum(tf.cast(tf.logical_and(tf.equal(y_true, 0), tf.equal(tf.round(y_pred), 1)), tf.float32))
    return tf.keras.losses.binary_crossentropy(y_true, y_pred) + 0.1 * false_positives

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss=custom_loss, metrics=['accuracy'])

# Define callbacks
checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max', verbose=2)
early_stopping = EarlyStopping(monitor='val_loss', patience=5, verbose=2)
custom_callback = CustomCallback()



print("training")
# Train the model with callbacks
history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    validation_steps=len(validation_generator),
    epochs=20,  # Increase the number of epochs
    validation_data=validation_generator,
    callbacks=[custom_callback, checkpoint, early_stopping],  # Corrected callback name
    verbose=2  # Change verbose to 2 for more detailed output
)

# Save the model and architecture to a file
model.save('model_architecture_and_weights.h5')

# Save the model architecture to a JSON file (optional)
with open('model_architecture.json', 'w') as json_file:
    json_file.write(model.to_json())
