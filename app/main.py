import flask
import neuralgym
from inpaint_model import InpaintCAModel
from uri_encoder import decode_uri_to_image, encode_image_to_uri
from preprocess_image import preprocess_image
import tensorflow as tf
import cv2
import io
from PIL import Image

app = flask.Flask(__name__)

FLAGS = neuralgym.Config('inpaint.yml')
model = InpaintCAModel()


@app.route("/RemoveImageWatermark", methods=["POST"])
def remove_image_watermark():
    if not flask.request.is_json:
        return flask.jsonify({"error": "Request payload must be JSON"}), 400
    body = flask.request.get_json()
    sourceURI = body.get("sourceURI")
    image = decode_uri_to_image(sourceURI)
    input_image = preprocess_image(image, "istock")
    tf.reset_default_graph()
    sess_config = tf.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    if input_image.shape == (0,):
        return flask.jsonify({"error": "Invalid image"}), 400
    with tf.Session(config=sess_config) as sess:
        input_image = tf.constant(input_image, dtype=tf.float32)
        output = model.build_server_graph(FLAGS, input_image)
        output = (output + 1.) * 127.5
        output = tf.reverse(output, [-1])
        output = tf.saturate_cast(output, tf.uint8)
        # load pretrained model
        vars_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
        assign_ops = []
        for var in vars_list:
            vname = var.name
            from_name = vname
            var_value = tf.contrib.framework.load_variable(
                "/root/watermark-removal/model/", from_name
            )
            assign_ops.append(tf.assign(var, var_value))
        sess.run(assign_ops)
        print('Model loaded.')
        result = sess.run(output)
        ok, encoded_image = cv2.imencode(".png", cv2.cvtColor(
            result[0][:, :, ::-1], cv2.COLOR_BGR2RGB)
        )
        if not ok:
            return flask.jsonify({"error": "Failed to encode image"}), 500

        return flask.jsonify({"targetURI": encode_image_to_uri(
            Image.open(io.BytesIO(encoded_image.tobytes())),
            "png"
        )})
