
import logging
import os
import sys

from tqdm import tqdm

logger = logging.getLogger(__name__)

class InputExample(object):
    """A single training/test example for simple sequence classification."""

    def __init__(self, guid, text, label=None):
        self.guid = guid
        self.text = text 
        self.label = label

class InputFeatures(object):
    """A single set of features of data."""

    def __init__(self, input_ids, input_mask, segment_ids, label_id, ori_tokens):

        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids
        self.label_id = label_id
        self.ori_tokens = ori_tokens


class NerProcessor(object):

    def read_data(self, input_file):

        with open(input_file, "r", encoding="utf-8") as f:
            lines = []
            words = []
            labels = []
            
            for line in f.readlines():
                
                contends = line.strip()
                tokens = line.strip().split("\t")

                if len(tokens) == 2:
                    words.append(tokens[0])
                    labels.append(tokens[1])
                else:
                    if len(contends) == 0:
                        l = " ".join([label for label in labels if len(label) > 0])
                        w = " ".join([word for word in words if len(word) > 0])
                        lines.append([l, w])
                        words = []
                        labels = []
            
            return lines
    
    def get_labels(self):
        return ["O", "B", "I"]

    def get_examples(self, input_file):
        examples = []
        
        lines = self.read_data(input_file)

        for i, line in enumerate(lines):
            guid = str(i)
            text = line[1]
            label = line[0]

            examples.append(InputExample(guid=guid, text=text, label=label))
        
        return examples


def convert_examples_to_features(args, examples, label_list, max_seq_length, tokenizer):

    label_map = {label : i for i, label in enumerate(label_list)}

    features = []

    for (ex_index, example) in tqdm(enumerate(examples), desc="convert examples"):
        # if ex_index % 10000 == 0:
        #     logger.info("Writing example %d of %d" % (ex_index, len(examples)))
        
        textlist = example.text.split(" ")
        labellist = example.label.split(" ")
        assert len(textlist) == len(labellist)
        tokens = []
        labels = []
        ori_tokens = []

        for i, word in enumerate(textlist):
            # 防止wordPiece情况出现，不过貌似不会
            
            token = tokenizer.tokenize(word)
            tokens.extend(token)
            label_1 = labellist[i]
            ori_tokens.append(word)

            # 单个字符不会出现wordPiece
            for m in range(len(token)):
                if m == 0:
                    labels.append(label_1)
                else:
                    if label_1 == "O":
                        labels.append("O")
                    else:
                        labels.append("I")
            
        if len(tokens) >= max_seq_length - 1:
            tokens = tokens[0:(max_seq_length - 2)]  # -2 的原因是因为序列需要加一个句首和句尾标志
            labels = labels[0:(max_seq_length - 2)]
            ori_tokens = ori_tokens[0:(max_seq_length - 2)]

        ori_tokens = ["[CLS]"] + ori_tokens + ["[SEP]"]
        
        ntokens = []
        segment_ids = []
        label_ids = []
        ntokens.append("[CLS]")
        segment_ids.append(0)
        label_ids.append(label_map["O"])

        for i, token in enumerate(tokens):
            ntokens.append(token)
            segment_ids.append(0)
            label_ids.append(label_map[labels[i]])

        ntokens.append("[SEP]")
        segment_ids.append(0)
        label_ids.append(label_map["O"])
        input_ids = tokenizer.convert_tokens_to_ids(ntokens)   
        
        input_mask = [1] * len(input_ids)

        assert len(ori_tokens) == len(ntokens), f"{len(ori_tokens)}, {len(ntokens)}, {ori_tokens}"

        while len(input_ids) < max_seq_length:
            input_ids.append(0)
            input_mask.append(0)
            segment_ids.append(0)
            # we don't concerned about it!
            label_ids.append(0)
            ntokens.append("**NULL**")

        assert len(input_ids) == max_seq_length
        assert len(input_mask) == max_seq_length
        assert len(segment_ids) == max_seq_length
        assert len(label_ids) == max_seq_length

        if ex_index < 5:
            logger.info("*** Example ***")
            logger.info("guid: %s" % (example.guid))
            logger.info("tokens: %s" % " ".join(
                [str(x) for x in ntokens]))
            logger.info("input_ids: %s" % " ".join([str(x) for x in input_ids]))
            logger.info("input_mask: %s" % " ".join([str(x) for x in input_mask]))
            logger.info("segment_ids: %s" % " ".join([str(x) for x in segment_ids]))
            logger.info("label_ids: %s" % " ".join([str(x) for x in label_ids]))

        # if not os.path.exists(os.path.join(output_dir, 'label2id.pkl')):
        #     with open(os.path.join(output_dir, 'label2id.pkl'), 'wb') as w:
        #         pickle.dump(label_map, w)

        features.append(
                InputFeatures(input_ids=input_ids,
                              input_mask=input_mask,
                              segment_ids=segment_ids,
                              label_id=label_ids,
                              ori_tokens=ori_tokens))

    return features