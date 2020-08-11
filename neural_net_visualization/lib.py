LOSS_FUNC_NAMES = ['Binary Crossentropy', 'Focal Loss']
FL_GAMMA = 2.0
FL_ALPHA = 0.75
LEARNING_RATE = 0.001
SIGMOID_THD = 0.2

# descriptor for what's in the test/training TFRecord files
TFREC_DESCRIPTOR = {
    'image'                        : tf.io.FixedLenFeature([], tf.string),
    'image_name'                   : tf.io.FixedLenFeature([], tf.string),
    'patient_id'                   : tf.io.FixedLenFeature([], tf.int64),
    'sex'                          : tf.io.FixedLenFeature([], tf.int64),
    'age_approx'                   : tf.io.FixedLenFeature([], tf.int64),
    'anatom_site_general_challenge': tf.io.FixedLenFeature([], tf.int64),
    'target'                       : tf.io.FixedLenFeature([], tf.int64)
} 
UNLABELED_TFREC_DESCRIPTOR = dict(TFREC_DESCRIPTOR)
del UNLABELED_TFREC_DESCRIPTOR['target']


class TFRECParser:
    """Class to parse the TFRecord files that come with the original dataset.
    """
    __TFREC_DESCRIPTOR = TFREC_DESCRIPTOR

    def __init__(self) -> None:
        self.__dataset = None # tf.data.TFRecordDataset

    @tf.autograph.experimental.do_not_convert
    def load(self, path_tfrec: str = 'tfrecords/train*.tfrec') -> None:
        def parser(serialized_example: Example) -> Example:
            example = tf.io.parse_single_example(serialized_example,
                                                 features=TFRECParser.__TFREC_DESCRIPTOR)
            return example
        self.__dataset = tf.data.TFRecordDataset(tf.io.gfile.glob(path_tfrec))
        self.__dataset = self.__dataset.map(parser)

    def get_dataset(self) -> tf.data.Dataset:
        return self.__dataset

    def get_image_arr(self, image_name: str) -> np.ndarray:
        record_dataset = self.__dataset.filter(lambda example: tf.equal(example["image_name"], image_name))
        example = next(iter(record_dataset))
        arr = tf.image.decode_jpeg(example['image'], channels=3).numpy()
        return arr

    def get_image(self, image_name: str) -> Image:
        return Image.fromarray(self.get_image_arr(image_name))

    def plot_image(self, image_name: str, 
                   figsize: list = [5, 5], 
                   ax: plt.axes = None,
                   show_info: bool = False) -> Image:
        img_arr = self.get_image_arr(image_name)
        img = Image.fromarray(img_arr)

        # prep title
        if show_info:
            title = "{}, {}x{}, {:.2f}MB".format(image_name,
                                                img.size[0],
                                                img.size[1],
                                                sys.getsizeof(img_arr)/1024/1024)
        else:
            title = image_name

         # render plot
        if ax is None:
            plt.figure(figsize=figsize)
            io.imshow(img_arr)
            plt.title(title)
            plt.show()
        else:
            ax.imshow(img_arr)
            ax.set_title(title)
    
    def plot_images(self, img_names: list, title: str = None) -> None:
        if len(img_names) == 1:
            self.plot_image(img_names[0])
            return

        PLOT_COL_COUNT = 7

        img_names = img_names.copy()

        n = len(img_names)
        row_count = n // PLOT_COL_COUNT
        if n % PLOT_COL_COUNT != 0 or row_count == 0:
            row_count += 1

        if row_count > 1:
            fig, axes = plt.subplots(row_count, 
                                     PLOT_COL_COUNT,
                                     figsize=(PLOT_COL_COUNT*3, row_count*3))
            if title is not None:
                fig.suptitle(title, fontsize=16)
                
            for row in axes:
                for ax in row:
                    # style
                    ax.get_xaxis().set_visible(False)
                    ax.get_yaxis().set_visible(False)

                    # render
                    if len(img_names) > 0:
                        self.plot_image(img_names.pop(), ax=ax)
        else:
             fig, axes = plt.subplots(1, n, figsize=(n*4, 4))
             if title is not None:
                 fig.suptitle(title, fontsize=16)

             for ax in axes:
                 # style
                 ax.get_xaxis().set_visible(False)
                 ax.get_yaxis().set_visible(False)

                 # render
                 self.plot_image(img_names.pop(), ax=ax)

def read_labeled_tfrecord(example: Example, 
                          return_targets: bool = True,
                          return_images: bool = True) -> Tuple['tf.string', 'tf.int64']:
    """Extract image & label from the tfrecord.
    """   
    example = tf.io.parse_single_example(example, TFREC_DESCRIPTOR)
    
    if return_images and return_targets:
        return example['image'], example['target']

    if return_images:
        return example['image']
        
    if  return_targets:
        return example['target']
    

def read_meta_tfrecord(example: Example, 
                       return_targets: bool = True) -> Tuple['tf.string', 'tf.int64']:
    """Extract meta & label from the tfrecord.
    """
    # age
    # mean: NaN, not ideal but simple
    # ---
    # sex:
    # -1: NaN
    # 0:'male`
    # 1:'female`
    # ---
    # anatom_site_general_challenge:
    # -1: NaN
    # 0: 'head/neck' 
    # 1: 'upper extremity'
    # 2: 'lower extremity'
    # 3: 'torso',
    # 4: 'palms/soles'
    # 5: 'oral/genital'
    if return_targets:
        example = tf.io.parse_single_example(example, TFREC_DESCRIPTOR)
    else:
        example = tf.io.parse_single_example(example, UNLABELED_TFREC_DESCRIPTOR)
    
    age = [example['age_approx']]
    sex = tf.one_hot(indices=example['sex'], 
                     depth=2, 
                     dtype=tf.int64)
    anat = tf.one_hot(indices=example['anatom_site_general_challenge'], 
                      depth=6,
                      dtype=tf.int64)
    x = tf.concat([age, sex, anat], axis=0)

    if return_targets:
        y = example['target']
        return (x, y)
    else:
        return (x, -1)

def read_unlabeled_tfrecord(example: Example, 
                            return_img_name: bool = False) -> Tuple['tf.string', 'tf.int64']:
    """Label is unavailable, extract image & image name from the tfrecord.
    """
    tfrec_format = {
        'image'                        : tf.io.FixedLenFeature([], tf.string),
        'image_name'                   : tf.io.FixedLenFeature([], tf.string),
    }
    example = tf.io.parse_single_example(example, tfrec_format)
    if return_img_name:
        return example['image'], example['image_name']
    else:
        return example['image'], 0

def aug_image(img, augment=True, dim=256):
    """Apply random transformation.
    """
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.cast(img, tf.float32) / 255.0
    
    if augment:
        img = tf.image.random_flip_left_right(img)
        img = tf.image.random_flip_up_down(img)
        img = tf.image.random_hue(img, 0.05)
        img = tf.image.random_saturation(img, 0.8, 1.2)
        img = tf.image.random_contrast(img, 0.8, 1.2)
        img = tf.image.random_brightness(img, 0.1)
        img = tf.clip_by_value(img, 0.0, 1.0)
                      
    img = tf.reshape(img, [dim,dim, 3])
            
    return img

def count_examples(file_names: List[str]):
    """Note that the name of each tfrecord file is sufixed with the number of 
    images included.
    """
    n = [int(re.compile(r"-([0-9]*)\.").search(f).group(1)) 
         for f in file_names]
    return np.sum(n)
                  
def get_dual_dataset(tfrec_files: List[str], 
                     dim: int,
                     batch_size: int = 64,
                     augment: bool = False, 
                     shuffle: bool = False, 
                     shuffle_seed: int = None, 
                     repeat: bool = False, 
                     labeled: bool=True,
                     drop_remainder: bool = False,
                     meta: bool = False) -> Tuple[tf.data.TFRecordDataset, 
                                               tf.data.TFRecordDataset, 
                                               int]:
    """Exactly the same as get_dataset. The only difference is that a tuple of three 
    items will be returned.
        [0]: metadata
        [1]: images
        [2]: steps
    """
    if shuffle_seed is None:
        shuffle_seed = tf.convert_to_tensor(random.randint(0, 10000), 
                                            dtype=tf.dtypes.int64)
    
    ds_meta, _ = get_dataset(
                        tfrec_files=tfrec_files, 
                        dim=dim,
                        batch_size=batch_size,
                        augment=augment, 
                        shuffle=shuffle, 
                        shuffle_seed=shuffle_seed,
                        repeat=repeat, 
                        labeled=labeled,
                        drop_remainder=drop_remainder,
                        meta=True)
    ds_image, steps = get_dataset(
                        tfrec_files=tfrec_files, 
                        dim=dim,
                        batch_size=batch_size,
                        augment=augment, 
                        shuffle=shuffle, 
                        shuffle_seed=shuffle_seed,
                        repeat=repeat, 
                        labeled=labeled,
                        drop_remainder=drop_remainder,
                        meta=False) 
    
    return ds_meta, ds_image, steps

def get_dataset(tfrec_files: List[str], 
                dim: int,
                batch_size: int = 64,
                augment: bool = False, 
                shuffle: bool = False, 
                shuffle_seed: int = None, 
                repeat: bool = False, 
                return_img_names: bool = True,
                drop_remainder: bool = False,
                labeled: bool = True, 
                meta: bool = False) -> Tuple[tf.data.TFRecordDataset, int]:
    """Return a TFRecordDataset by loading tfrecord files.
    Returns:
        if meta == True:
            [0](TFRecordDataset): TFRecordDataset with keys 'meta' and 'target'. 
            [1](int): Number of steps to complete an epoch.
        if meta == False:
            [0](TFRecordDataset): TFRecordDataset with keys 'image' and 'target'. 
                Data of which depend on the follwing arguements:  
                    - label == True: 'target' will be filled. None otherwise.
                    - return_img_names == True: 
                        'image' will be filled with the image names instead of 
                        the actual image ndarray.
            [1](int): Number of steps to complete an epoch.
    """
    
    AUTO = tf.data.experimental.AUTOTUNE
    ds = tf.data.TFRecordDataset(tfrec_files, 
                                 num_parallel_reads=AUTO)
    ds = ds.cache()
    
    if not repeat:
        ds = ds.repeat(1)
    else:
        ds = ds.repeat(-1)

    if shuffle: 
        ds = ds.shuffle(buffer_size=1024, seed=shuffle_seed) # 1024 to optimize TPU performance
    
    if meta:
        # extract meta & label
        map_ = lambda example: read_meta_tfrecord(example, labeled)
        ds = ds.map(map_, num_parallel_calls=AUTO)
    else:
        if labeled: 
            # extract image & label
            # ds inlcudes just one column of examples
            ds = ds.map(read_labeled_tfrecord, num_parallel_calls=AUTO)
        else:
            # extract image & image name
            # ds inlcudes just one column of examples
            map_ = lambda example: read_unlabeled_tfrecord(example, return_img_names)
            ds = ds.map(map_, num_parallel_calls=AUTO)      
        
        # transform image
        map_ = lambda img, _: (aug_image(img, augment=augment, dim=dim), _)
        ds = ds.map(map_, num_parallel_calls=AUTO)
    
    # https://tinyurl.com/yao4obsb
    # A single Cloud TPU device consists of four chips, each of which has two TPU cores. 
    # Therefore, for efficient utilization of Cloud TPU, a program should make use of 
    # each of the eight cores.
    #
    # https://tinyurl.com/y99kjyh5
    # Model processing performance
    # For optimum memory usage, use the largest batch size that will fit in memory. 
    # Each TPU core uses a 128 x 128 memory cell matrix for processing. In general, 
    # your batch sized should be evenly divisible by 128 to most effectively use the TPU memory.
    #
    # https://tinyurl.com/yawn2acn
    # Batch Size Too Small
    # The batch size of any model should always be at least 64 (8 per TPU core) 
    # because TPU always pads the tensors to this size. The ideal batch size when 
    # training on the TPU is 1024 (128 per TPU core), since this eliminates inefficiencies 
    # related to memory transfer and padding.
    #
    # https://tinyurl.com/y9nojpa2
    # Minimal requirement: A multiple of 8!
    if PROCESSOR == 'TPU':
        if batch_size < 64:
            # better
            print('Warning: Batch size {} is smaller than 64...'.format(batch_size))
        if batch_size % 8 > 0:
            # min requirement
            print('Error: Batch size {} is not a multiple of 8...'.format(batch_size))
    ds = ds.batch(batch_size, drop_remainder=drop_remainder) 
    
    num_images = count_examples(tfrec_files)
    steps = num_images // batch_size
    if num_images % batch_size > 0:
        # require one more step to loop through the entire dataset
        steps += 1
    
    # From tf doc (https://tinyurl.com/yavczqkr):
    # Most dataset input pipelines should end with a call to prefetch. This allows 
    # later elements to be prepared while the current element is being processed. This 
    # often improves latency and throughput, at the cost of using additional memory to 
    # store prefetched elements.
    ds = ds.prefetch(AUTO)
    
    return ds, steps

def focal_loss(gamma: float = 2., alpha: float = .25) -> callable:
    """Soruces:
            https://tinyurl.com/y4e66a44
            https://tinyurl.com/yyudyorg
    """
    def focal_loss_fixed(y_true, y_pred):
        pt_1 = tf.where(tf.equal(y_true, 1), y_pred, tf.ones_like(y_pred))
        pt_0 = tf.where(tf.equal(y_true, 0), y_pred, tf.zeros_like(y_pred))
        return -K.mean(alpha * K.pow(1. - pt_1, gamma) * K.log(pt_1)) - K.mean((1 - alpha) * K.pow(pt_0, gamma) * K.log(1. - pt_0))
    return focal_loss_fixed

def build_efns(dim: int, 
               ef: int, 
               loss: int = 0,
               sig_thd: float = SIGMOID_THD,
               fl_gamma: float = FL_GAMMA,
               fl_alpha: float = FL_ALPHA,
               lr: float = LEARNING_RATE) -> Sequential:

    EFNS = [efn.EfficientNetB0, 
            efn.EfficientNetB1, 
            efn.EfficientNetB2, 
            efn.EfficientNetB3, 
            efn.EfficientNetB4, 
            efn.EfficientNetB5, 
            efn.EfficientNetB6,
            efn.EfficientNetB7]
    LOSS_FS = [keras.losses.BinaryCrossentropy(label_smoothing=0.05),
               focal_loss(fl_gamma, fl_alpha)]
    
    m = Sequential()
    base = EFNS[ef](weights="imagenet", 
                    include_top=False, 
                    input_shape=(dim, dim, 3))
    m.add(base)
    m.add(GlobalAveragePooling2D())
    m.add(Dense(1, activation="sigmoid"))
    
    # compile model
    m.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), 
              loss=LOSS_FS[loss], 
              metrics=[AUC(),
                       BinaryAccuracy(threshold=sig_thd),
                       Recall(thresholds=sig_thd)])

    return m

def build_efn_metann(dim: int, 
                     ef: int, 
                     loss: int = 0,
                     sig_thd: float = SIGMOID_THD,
                     fl_gamma: float = FL_GAMMA,
                     fl_alpha: float = FL_ALPHA,
                     lr: float = LEARNING_RATE) -> Sequential:
    DROP_OUT_RATE = 0.5

    # How EfficientNet scale? https://tinyurl.com/yxk355ye
    EFNS = [efn.EfficientNetB0, 
            efn.EfficientNetB1, 
            efn.EfficientNetB2, 
            efn.EfficientNetB3, 
            efn.EfficientNetB4, 
            efn.EfficientNetB5, 
            efn.EfficientNetB6,
            efn.EfficientNetB7]
    LOSS_FS = [keras.losses.BinaryCrossentropy(label_smoothing=0.05),
               focal_loss(fl_gamma, fl_alpha)]
    
    # building EfficientNet
    m_efn = Sequential()
    base = EFNS[ef](weights="imagenet", 
                    include_top=False, 
                    input_shape=(dim, dim, 3))
    m_efn.add(base)
    m_efn.add(GlobalAveragePooling2D())

    # building nn for metadata
    # input_dim = age + sex + anatom = 1 + 2 + 6 = 9
    # order of dense, activation, BatchNorm, Drop-out, etc.: https://tinyurl.com/y3a2w3n7
    m_metann = Sequential()
    m_metann.add(Dense(32, input_dim=9, activation='relu'))
    m_metann.add(BatchNormalization())
    m_metann.add(Dropout(DROP_OUT_RATE))
    
    m_metann.add(Dense(32, activation='relu'))
    m_metann.add(BatchNormalization())
    m_metann.add(Dropout(DROP_OUT_RATE))
    
    # concatenate the two outputs 
    # https://tinyurl.com/y3e7yhgm
    # https://tinyurl.com/y4s5qzuy
    concat = Concatenate()([m_efn.output, m_metann.output])
    concat = Dense(512, activation='relu')(concat)
    concat = BatchNormalization()(concat)
    concat = Dropout(DROP_OUT_RATE)(concat)

    out = Dense(1, activation='sigmoid')(concat)

    # build and compile the full model
    m_final = Model(inputs=[m_metann.input, m_efn.input], outputs=out)
    m_final.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), 
                    loss=LOSS_FS[loss], 
                    metrics=[AUC(),
                             BinaryAccuracy(threshold=sig_thd),
                             Recall(thresholds=sig_thd)])
    return m_final

def dual_input_generator(meta: tf.data.TFRecordDataset, 
                         img: tf.data.TFRecordDataset) -> tuple:
    while True:
        # only works on GPU/CPU
        data_meta, _ = next(iter(meta))
        data_img, targets = next(iter(img))

        yield [data_meta, data_img], targets