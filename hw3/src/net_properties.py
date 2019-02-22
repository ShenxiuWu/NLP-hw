class NetProperties:
    def __init__(self, word_embed_dim, pos_embed_dim, label_embed_dim, hidden_first_dim, hidden_second_dim, minibatch_size):
        self.word_embed_dim = word_embed_dim
        self.pos_embed_dim = pos_embed_dim
        self.label_embed_dim = label_embed_dim
        self.hidden_first_dim = hidden_first_dim
        self.hidden_second_dim = hidden_second_dim
        self.minibatch_size = minibatch_size