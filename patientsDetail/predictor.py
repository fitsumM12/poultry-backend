# ml/models.py
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adamax
from django.conf import settings
import os

from keras import regularizers
# entry flow
from tensorflow.keras.layers import Reshape, Multiply, Activation, Add, Input, ReLU, BatchNormalization, MaxPool2D, Dropout
from tensorflow.keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, GlobalAvgPool2D, SeparableConv2D

def conv_bn(x, filters, kernel_size, strides=1):

    x = Conv2D(filters=filters,
            kernel_size = kernel_size,
            strides=strides,
            padding = 'same',
            use_bias = False)(x)
    x = BatchNormalization()(x)
    return x

def sep_bn(x, filters, kernel_size, strides=1):

    x = SeparableConv2D(filters=filters,
                        kernel_size = kernel_size,
                        strides=strides,
                        padding = 'same',
                        use_bias = False)(x)
    x = BatchNormalization()(x)
    return x


def entry_flow(x):

    x = conv_bn(x, filters =32, kernel_size =3, strides=2)
    x = ReLU()(x)
    x = conv_bn(x, filters =64, kernel_size =3, strides=1)
    tensor = ReLU()(x)

    x = sep_bn(tensor, filters = 64, kernel_size =3)
    x = ReLU()(x)
    x = sep_bn(x, filters = 64, kernel_size =3)
    x = MaxPool2D(pool_size=3, strides=2, padding = 'same')(x)

    tensor = conv_bn(tensor, filters=64, kernel_size = 1,strides=2)
    x = Add()([tensor,x])

    x = ReLU()(x)
    x = sep_bn(x, filters =64, kernel_size=3)
    x = ReLU()(x)
    x = sep_bn(x, filters =64, kernel_size=3)
    x = MaxPool2D(pool_size=3, strides=2, padding = 'same')(x)

    tensor = conv_bn(tensor, filters=64, kernel_size = 1,strides=2)
    x = Add()([tensor,x])

    x = ReLU()(x)
    x = sep_bn(x, filters =64, kernel_size=3)
    x = ReLU()(x)
    x = sep_bn(x, filters =64, kernel_size=3)
    x = MaxPool2D(pool_size=3, strides=2, padding = 'same')(x)

    tensor = conv_bn(tensor, filters=64, kernel_size = 1,strides=2)
    x = Add()([tensor,x])
    return x

# middle flow

def middle_flow(tensor):

#     for _ in range(8):
    x = ReLU()(tensor)
    x = sep_bn(x, filters = 64, kernel_size = 3)
    x = ReLU()(x)
    x = sep_bn(x, filters = 64, kernel_size = 3)
    x = ReLU()(x)
    x = sep_bn(x, filters = 64, kernel_size = 3)
    x = ReLU()(x)
    tensor = Add()([tensor,x])
    return tensor
# exit flow

def exit_flow(tensor):

    x = ReLU()(tensor)
    x = sep_bn(x, filters = 64,  kernel_size=3)
    x = ReLU()(x)
    x = sep_bn(x, filters = 64,  kernel_size=3)
    x = MaxPool2D(pool_size = 3, strides = 2, padding ='same')(x)
    tensor = conv_bn(tensor, filters =64, kernel_size=1, strides =2)
    x = Add()([tensor,x])
    x = sep_bn(x, filters = 128,  kernel_size=3)
    x = ReLU()(x)
    x = sep_bn(x, filters = 128,  kernel_size=3)
    x = ReLU()(x)
    return x
def squeeze_excite_block(input_tensor, ratio=16):
    filters = input_tensor.shape[-1] 
    se = GlobalAveragePooling2D()(input_tensor)
    se = Dense(filters // ratio, activation='relu')(se)
    se = Dense(filters, activation='sigmoid')(se)
    se = Reshape((1, 1, filters))(se)
    x = Multiply()([input_tensor, se])
    return x

# def create_model():
#     input = Input(shape = (299,299,3))
#     x = entry_flow(input)
#     x = middle_flow(x)
#     output = exit_flow(x)
#     student_scratch = Model (inputs=input, outputs=output)
#     x = student_scratch.output
#     for i, layer in enumerate(student_scratch.layers):
#         if isinstance(layer, Conv2D):
#             x = squeeze_excite_block(x) 
#             x = ReLU()(x)
#     x = GlobalAvgPool2D()(x)
#     x = Dense(128,activation='relu')(x)
#     x = Dense(64,activation='relu')(x)
#     x = Dense(units=3, activation='softmax')(x)  
#     model = Model(inputs=student_scratch.input, outputs=x)
#     return model

def load_weights(model):
    weights_path = os.path.join(settings.MEDIA_ROOT_MODEL, '_xception_fold_1.h5')
    model.load_weights(weights_path)

def predict(model, image_data):
    predictions = model.predict(image_data)
    return predictions

def create_model():
    base_model = tf.keras.applications.Xception(
        weights='imagenet', include_top=False, input_shape=(512, 512, 3)
    )
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dense(
        128, 
        activation='relu', 
        kernel_regularizer=regularizers.l2(1e-2)
    )(x)
    x = tf.keras.layers.Dropout(1e-2)(x)
    predictions = tf.keras.layers.Dense(
        3, 
        activation='softmax', 
        kernel_regularizer=regularizers.l2(1e-2)
    )(x)
    model = tf.keras.Model(inputs=base_model.input, outputs=predictions)
    return model