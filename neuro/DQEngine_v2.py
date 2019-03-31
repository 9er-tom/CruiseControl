#import gym
import numpy as np
import tensorflow as tf
import matplotlib.pylab as plt
import random
import math
import InputFunctions
import OutputFunctions
import neuro.screengrab as screengrab
import neuro.Controller as controller
import os
import time

MAX_EPSILON = 0.9
MIN_EPSILON = 0.005
LAMBDA = 0.0001
GAMMA = 0.99
BATCH_SIZE = 250

class Model:
    def __init__(self, num_states, num_actions, batch_size): #num_actions = mögliche Aktionen  num_states = anzahl der Inputs
        self._num_states = num_states
        self._num_actions = num_actions
        print("States", num_states)
        self._batch_size = batch_size
        # define the placeholders
        self.inputlayer = None
        self._actions = None
        # the output operations
        self._logits = None
        self._optimizer = None
        self._var_init = None
        # now setup the model
        self._define_model()

    def _define_model(self):
        self.inputlayer = tf.placeholder(shape=[None, self._num_states], dtype=tf.float32)
        self.outputlayer = tf.placeholder(shape=[None, self._num_actions], dtype=tf.float32)
        #layer1 = tf.layers.conv2d()
        #layer2 = tf.layers
        # 2 vollverknüpfte hl 800n
        layer1 = tf.layers.dense(self.inputlayer, 800, activation=tf.nn.relu)
        layer2 = tf.layers.dense(layer1, 800, activation=tf.nn.relu)
        #fc3 = tf.layers.dense(layer2, 400, activation=tf.nn.relu)
        self._logits = tf.layers.dense(layer2, self._num_actions)
        loss = tf.losses.mean_squared_error(self.outputlayer, self._logits)
        self._optimizer = tf.train.AdamOptimizer().minimize(loss)
        self._var_init = tf.global_variables_initializer()

    def predict_one(self, state, sess):
        return sess.run(self._logits, feed_dict={self.inputlayer: state.reshape(1, self.num_states)})

    def predict_batch(self, states, sess):
        return sess.run(self._logits, feed_dict={self.inputlayer: states})

    def train_batch(self, sess, x_batch, y_batch):
        sess.run(self._optimizer, feed_dict={self.inputlayer: x_batch, self.outputlayer: y_batch})

    @property
    def num_states(self):
        return self._num_states

    @property
    def num_actions(self):
        return self._num_actions

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def var_init(self):
        return self._var_init


class Memory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []

    def add_sample(self, sample):
        self._samples.append(sample)
        if len(self._samples) > self._max_memory:
            self._samples.pop(0)
            print("MEMORY OVERFLOW!")

    def sample(self, no_samples):
        if no_samples > len(self._samples):
            return random.sample(self._samples, len(self._samples))
        else:
            return random.sample(self._samples, no_samples)


class Interpreter:
    def reset(self):
        OutputFunctions.kill() #OMG WENN DU INPUTS ÄNERST BITTE ÄNDER A DEN SCHEISS BRING MI UM
        #state = InputFunctions.get_info()
        #state= np.append(state, screengrab.grab_screen())
        #screengrab.reset()
        state = np.append(screengrab.grab_screen(),InputFunctions.get_speed())
        #print("Shape",state.shape)
        return state

    def step(self,action):
        #print(action)
        controller.hardcontrolfifteen(action)
        #inputs = InputFunctions.get_info()
        #next_state = inputs
        #screen = screengrab.grab_screen()
        next_state = np.append(screengrab.grab_screen(),InputFunctions.get_speed())
        #print(len(next_state))
        #next_state = np.append(inputs, screen)

        #print(next_state)
        reward = InputFunctions.calculatereward()
        done = False;
        if(not InputFunctions.checkOnTrack()):
            done = True
            if(InputFunctions.getlaps()>0):
                reward+=1000
                print("YOU DID IT")
            #else:
                #reward-=100

        info = 0 #möglicher Slot für AI Info
        return next_state, reward, done, info


class GameRunner:
    def __init__(self, sess, model, interpreter, memory, max_eps, min_eps,
                 decay, render=True):
        self._sess = sess
        self.interpr = interpreter
        self._model = model
        self._memory = memory
        self._render = render
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._decay = decay
        self._eps = self._max_eps
        self._steps = 0
        self._reward_store = []

    def run(self):
        posx = InputFunctions.getpos()
        while(posx == InputFunctions.getpos()):
            state = self.interpr.reset(self)
            OutputFunctions.usepedals(throttle=1)
            time.sleep(0.4)
            OutputFunctions.usepedals(brake=1)
        InputFunctions.resetlastabpos()
        tot_reward = 0
        #max_x = -100
        while True:
            action = self._choose_action(state)
            next_state, reward, done, info = self.interpr.step(self, action)
            '''if next_state[0] >= 0.1:
                reward += 10
            elif next_state[0] >= 0.25:
                reward += 20
            elif next_state[0] >= 0.5:
                reward += 100
            '''
            # Runde Abgeschlossen, oder fehlgeschlagen -> nächster Status = none || Speichergrüne
            if done:
                next_state = None

            self._memory.add_sample((state, action, reward, next_state))
            self._replay()

            # epsilon mit regression exponentiell annähern
            self._steps += 1
            self._eps = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) \
                                      * math.exp(-LAMBDA * self._steps)

            # nächster state + belohnung holen
            state = next_state
            tot_reward += reward

            # wenn das auto von der Strecke ist, oder eine Runde geschafft hat, schleife unterbrechen
            if done:
                #if(InputFunctions.getlaps()>=1):
                #    tot_reward+=1
                self._reward_store.append(tot_reward)
                #if()
                break

        print("Step {}, Total reward: {}, Eps: {}".format(self._steps, tot_reward, self._eps))
        #if (tot_reward>100000):
         #   OutputFunctions.momgetthecamera()
          #  exit(0)

    def _choose_action(self, state):
        epsspeed=InputFunctions.get_speed()
        if  epsspeed >= self._eps*1000 and epsspeed < 50.0:
            if random.random() < self._eps:
                return random.randint(0, self._model.num_actions - 1)
        else:
            print("Skipped epsilon")
        return np.argmax(self._model.predict_one(state, self._sess))

    def _replay(self):
        batch = self._memory.sample(self._model.batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._model.num_states)
                                 if val[3] is None else val[3]) for val in batch]) # Problem für übergroße Arrays...

        # mit den vorhandenen Staten Q(s,a) errechnen
        q_s_a = self._model.predict_batch(states, self._sess)
        # ableiten von Q(s,a) zu Q(s',a') - um gamma * max(Q(s'a')) auszuführen
        q_s_a_d = self._model.predict_batch(next_states, self._sess)
        # trainingstabelle erstellen
        x = np.zeros((len(batch), self._model.num_states))
        y = np.zeros((len(batch), self._model.num_actions))
        for i, b in enumerate(batch):
            state, action, reward, next_state = b[0], b[1], b[2], b[3]
            # q values für jeden status errechnen
            current_q = q_s_a[i]
            # q values für jeder action errechnen
            if next_state is None:
                # ende der runde max Q(s',a') wird errechnet
                # prediction possible
                current_q[action] = reward
            else:
                current_q[action] = reward + GAMMA * np.amax(q_s_a_d[i]) # Q(s',a') wird errechnet
            x[i] = state
            y[i] = current_q
        self._model.train_batch(self._sess, x, y)

    @property
    def reward_store(self):
        return self._reward_store

    @property
    def max_x_store(self):
        return self._max_x_store

if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    num_states = 1601 #1601 #(2**1600)*250 #sind das states, oder inputs? 1600 wegen bild, (4 reifen) Wheelloads near to useless, 1 geschwindigkeit
    num_actions = 49 #49 mögliche aktionen
    num_actions = 15  # 15 mögliche aktionen
    #num_actions = 9  # 9 mögliche aktionen
    with tf.device("/gpu:0"):
        inter = Interpreter
        model = Model(num_states, num_actions, BATCH_SIZE)
        mem = Memory(1600000) #1,6 mill memory
        saver = tf.train.Saver()
        config = tf.ConfigProto(allow_soft_placement=True)
        #sess = tf.Session(config=config)
        with tf.Session(config=config) as sess:
            time.sleep(5)
            #if(os.path.exists("D:/saves/model.ckpt"
            saver.restore(sess, "D:/saves15/model.ckpt")
            print("Model restored.")
            print(sess.run(model.var_init))
            gr = GameRunner(sess, model, inter, mem, MAX_EPSILON, MIN_EPSILON, LAMBDA)
            iterations = 10000000
            cnt = 0
            while cnt < iterations:
                if cnt % 25 == 0:
                    save_path = saver.save(sess, "D:/saves15/model.ckpt")
                    print('Episode {} of {}'.format(cnt + 1, iterations))
                    print("Model saved in path: %s" % save_path)
                if InputFunctions.getbestlap() <= 230000 and InputFunctions.getbestlap() > 0:
                    print("Laptime reached",InputFunctions.getbestlap())
                    break
                gr.run()
                #OutputFunctions.usepedals(throttle=0)
                cnt += 1
            plt.plot(gr.reward_store)
            plt.show()
            plt.close("all")
            #plt.plot(gr.max_x_store)
            plt.show()

