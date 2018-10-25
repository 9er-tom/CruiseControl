import tensorflow as tf
import numpy as np
from neuro.Controller import control
import InputFunctions
import neuro.screengrab as scgrb
import InputFunctions

inputvars = 0
reaktionen = 0
klatschs = 0
rea = 0
Ylogits =0

def init():
    global  inputvars
    global klatschs
    global reaktionen
    global rea
    global Ylogits
    inputvars = tf.placeholder(shape=[None, 40*40 + 4 + 1 + 1],dtype = tf.float32 , name='X1') #pixel + 4x Reifenbelastung + relgeschwindigkeit(250,0,-100,1,0,-1) + Streckenfortschritt
    reaktionen = tf.placeholder(shape=[None],dtype=tf.int32, name='H1')
    klatschs = tf.placeholder(shape=[None],dtype=tf.int32, name='S1')

    Y = tf.layers.dense(inputvars, 200 , activation = tf.nn.relu)#single dense HL (vielleicht 2 hidden layer daraus machen?)
    Ylogits = tf.layers.dense(Y, 20*5*5)

    rea = tf.multinomial(logits=Ylogits, num_samples=1) #erstellt eine ream aus output mit softmax

def train():
    global  inputvars
    global klatschs
    global reaktionen
    global rea
    global Ylogits
    #train ( trennen?)
    crossent = tf.losses.softmax_cross_entropy(onehot_labels=tf.one_hot(reaktionen, 20*5*5, logits=Ylogits))

    loss = tf.reduce_sum(klatschs * crossent)

    #trainingstart
    optimierer = tf.train.RMSPropOptimizer(learning_rate=0.001, decay=0.99)
    train_rea = optimierer.minimize(loss)

    with tf.Session() as sess:
        #reset
        ontrack = True
        while ontrack: #while not gwatscht
            inputvar = scgrb.process_image()
            inputvar.extend(InputFunctions.get_info())
            ontrack=InputFunctions.checkOnTrack()


            reaktion = sess.run(rea, feed_dict={inputvars: [inputvar]})

            #step and get klatschs
            print(reaktion)
            control(reaktion)
            klatsch = 0

            inputvars.append(inputvar)
            reaktionen.append(reaktion)
            klatschs.append(klatsch)



