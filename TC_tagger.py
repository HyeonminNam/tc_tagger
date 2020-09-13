from konlpy_tc.tag import Okt_edit
import emoji
import re
import pandas as pd


class TC_tagger():

    def __init__(self):
        self.emoji_dic = emoji.UNICODE_EMOJI
        self.emoji_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.re_emoji = re.compile('|'.join(re.escape(p) for p in self.emoji_list))
        self.okt_edit = Okt_edit()
        
       

    def emoticon(self, result):
        emo_lst = []
        for idx, (token, _) in enumerate(result):
            if re.search(self.re_emoji, token):
                lst = [(x+'_'+self.emoji_dic[x][1:-1], 'Emoji') for x in token]
                emo_lst.append((idx, lst))
        emo_lst.reverse()
        for idx, emo in emo_lst:
            result.pop(idx)
            result[idx:idx] = emo
        return result
    
    def hashtag(self, result):
        for idx, (token, tag) in enumerate(result):
            if tag == 'Hashtag':
                phrase = self.okt_edit.phrases(token[1:])[0]
                new_token = re.sub(phrase, ' '+phrase+' ' , token[1:]).strip().split()
                h = []
                for x in new_token:
                    if x == phrase:
                        h.append((x, 'Hashtag_Noun'))
                    else:
                        tmp = self.okt_edit.pos(x)
                        for token, tag in tmp:
                            h.append((token, 'Hashtag_'+tag))         
                result[idx] = tuple(h)
        return result

    def tag(self, text):
        result = self.okt_edit.pos(text)
        result = self.emoticon(result)
        result = self.hashtag(result)
        return result

    def tokenizer(self, text):
        tag_result = self.tag(text)
        token_lst = []
        for x in tag_result:
            if type(x[0]) == str:
                token_lst.append(x[0])
            else:
                for y in x:
                    token_lst.append(y[0])
        return token_lst

    def nouns(self, text):
        tag_result = self.tag(text)
        nouns_lst = []
        for x in tag_result:
            if type(x[0]) == str and x[1] == 'Noun':
                nouns_lst.append(x[0])
            elif type(x[0]) == str:
                pass
            else:
                for y in x:
                    if y[1] == 'Hashtag_Noun':
                        nouns_lst.append(y[0])
        return nouns_lst

if __name__ == "__main__":
    text1 = '다이어트 해야되는데...😂 #멋짐휘트니스연산점 #연산동pt'
    text2 = '럽스타 그자체❤❤\n#럽스타그램 #운동하는커플 #태닝'
    text3 = '이지부스트 신은 연영과 학생'
    tc_tagger = TC_tagger()
    for t in [text1, text2, text3]:
        print('='*100)
        print('\nThreecow : ', tc_tagger.tag(t))
        print('\n', '='*100)
        print('\ntokenize 결과: ')
        print(tc_tagger.tokenizer(t))
        print('\nnouns 추출 결과: ')
        print(tc_tagger.nouns(t))