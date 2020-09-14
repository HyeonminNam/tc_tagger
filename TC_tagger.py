#-*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(__file__))
from konlpy_tc.tag import Okt_edit
import emoji
import re
from TC_preprocessing import Preprocessing


class Tagger():

    def __init__(self):
        self.emoji_dic = emoji.UNICODE_EMOJI
        self.emoji_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.re_emoji = re.compile('|'.join(re.escape(p) for p in self.emoji_list if p != '\u200d|\u200c'))
        self.okt_edit = Okt_edit()
        self.re_hashtag = re.compile('')
        self.preprocess = Preprocessing()
        

    # 이모지에 'Emoji' 태깅 붙여주는 함수
    def _emoticon(self, result):
        emo_lst = []
        for idx, (token, tag) in enumerate(result):
            emojis = re.findall(self.re_emoji, token)
            if emojis:
                if result[idx-1][0]=='#':
                    try:
                        lst = [(x+'_'+self.emoji_dic[x][1:-1], 'Hashtag_Emoji') for x in emojis]
                        emo_lst.append((idx-1, lst))
                        result.pop(idx-1)
                    except:
                        pass
                else:
                    try:
                        lst = [(x+'_'+self.emoji_dic[x][1:-1], 'Emoji') for x in emojis]
                        emo_lst.append((idx, lst))
                    except:
                        pass
        emo_lst.reverse()
        for idx, emo in emo_lst:
            result.pop(idx)
            result[idx:idx] = emo
        return result
    
    # 해쉬태그 분석하고 해쉬태그 고유명사 처리 알고리즘 수행하는 함수
    def _hashtag(self, result):
        for idx, (token, tag) in enumerate(result):
            if tag == 'Hashtag':
                token = re.search('[#](\w+)', token).group(1)
                phrase_lst = self.okt_edit.phrases(token)
                h = []
                if len(phrase_lst) == 0:
                    tmp = self.okt_edit.pos(token)
                    for token_, tag_ in tmp:
                        h.append((token_, 'Hashtag_'+tag_))
                else:
                    phrase = phrase_lst[0]
                    new_token = re.sub(phrase, ' '+phrase+' ' , token).strip().split()
                    h = []
                    for x in new_token:
                        if x == phrase and re.search('[가-힣ㄱ-ㅎㅏ-ㅣ]+', x):
                            h.append((x, 'Hashtag_Noun'))
                        else:
                            tmp = self.okt_edit.pos(x)
                            for token_, tag_ in tmp:
                                h.append((token_, 'Hashtag_'+tag_))
                result.pop(idx)         
                result[idx:idx] = h
        return result

    # 형태소 분석 함수
    def tag(self, text):
        text = self.preprocess.del_escape(text)
        try:
            result = self.okt_edit.pos(text)
            result = self._emoticon(result)
            result = self._hashtag(result)
        except Exception as e:
            print(e)
            return False
        return result

    # 토큰화 함수
    def tokenizer(self, text):
        tag_result = self.tag(text)
        if not tag_result:
            print('input is not valid!')
            return
        token_lst = []
        for x in tag_result:
            token_lst.append(x[0])
        return token_lst

    # 원하는 품사의 토큰들만 추출하는 함수
    def pos_filter(self, text, pos=['Noun', 'Hashtag_Noun']):
        pos_re = re.compile('|'.join(re.escape(p) for p in pos))
        tag_result = self.tag(text)
        if not tag_result:
            print('input is not valid!')
            return
        token_lst = []
        for x in tag_result:
            if pos_re.match(x[1]):
                token_lst.append(x[0])
        return token_lst

if __name__ == "__main__":
    text1 = '다이어트 해야되는데... #😂❤ #멋짐휘트니스연산점 #연산동pt'
    text2 = '럽스타 그자체❤❤\n#럽스타그램 #운동하는커플 #태닝'
    text3 = '#drive #eat'
    tc_tagger = Tagger()
    print(tc_tagger.tag(text1))
    print(tc_tagger.tag(text2))
    print(tc_tagger.tag(text3))
    # for t in [text1, text2, text3]:
    #     print('='*100)
    #     print('\nThreecow : ', tc_tagger.tag(t))
    #     print('\n', '='*100)
    #     print('\ntokenize 결과: ')
    #     print(tc_tagger.tokenizer(t))
    #     print('\n특정 품사 추출 결과: ')
    #     print(tc_tagger.pos_filter(t, pos=['Noun', 'Hashtag_Noun', 'Emoji']))