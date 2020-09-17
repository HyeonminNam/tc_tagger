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
    
    # 해시태그 분석하고 해시태그 고유명사 처리 알고리즘 수행하는 함수
    def _hashtag(self, result):
        h = []
        for pos_idx, (token, tag) in enumerate(result):
            if tag == 'Hashtag':
                try:
                    token = re.search('[#](.+)', token).group(1)
                except Exception as e:
                    print(e)
                    print(token)
                token_lst = self.okt_edit.pos(token)
                noun_idx_lst = [idx for idx, (token_, tag_) in enumerate(token_lst) if tag_ == 'Noun']
                if len(noun_idx_lst) >= 2:
                    np_idx =  []
                    tmp = []
                    v = noun_idx_lst.pop(0)
                    tmp.append(v)
                    while len(noun_idx_lst) > 0:
                        vv = noun_idx_lst.pop(0)
                        if v+1 == vv:
                            tmp.append(vv)
                            v = vv
                        else:
                            np_idx.append(tmp)
                            tmp = []
                            tmp.append(vv)
                            v = vv
                    np_idx.append(tmp)
                    np_idx.reverse()
                    for np in np_idx:
                        start, end = np[0], np[-1]
                        noun = ''
                        for n in np:
                            noun += token_lst[n][0]
                        token_lst[start] = (noun, 'Noun')
                        del token_lst[start+1:end+1]
                for idx, x in enumerate(token_lst):
                    token_lst[idx] = (x[0], 'Hashtag_' + x[1])
                h.append([pos_idx, token_lst])
        h.reverse()
        for pos_idx, token_lst in h:
            result.pop(pos_idx)
            result[pos_idx:pos_idx] = token_lst
        return result
    
    # Okt에서 인식 못하는 해시태그 처리
    def _punctuation_sharp(self, result):
        hash_lst = []
        for idx, x in enumerate(result):
            if x == ('#', 'Punctuation'):
                try:
                    hash_lst.append([idx, (result[idx+1][0], 'Hashtag_' + result[idx+1][1])])
                except:
                    return result
        hash_lst.reverse()
        for idx, hash_ in hash_lst:
            result.pop(idx)
            result[idx] = hash_
        return result

    # 형태소 분석 함수
    def tag(self, text):
        text = self.preprocess.del_escape(text)
        text = re.sub('(?P<match>[^\s])#', '\g<match> #', text) 
        try:
            result = self.okt_edit.pos(text)
            result = self._emoticon(result)
            result = self._hashtag(result)
            if ('#', 'Punctuation') in result:
                result = self._punctuation_sharp(result)
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
    text1 = '다이어트 해야되는데...😂😂 #멋짐휘트니스연산점 #연산동pt'
    text2 = '럽스타 그자체...❤❤\n#럽스타그램 #운동하는커플 #태닝'
    text3 = '#넓은카페#예쁜양말쇼핑'
    tc_tagger = Tagger()
    print(tc_tagger.tag(text3))
    # for t in [text1, text2, text3]:
    #     print('='*100)
    #     print('\nThreecow : ', tc_tagger.tag(t))
    #     print('\n', '='*100)
    #     print('\ntokenize 결과: ')
    #     print(tc_tagger.tokenizer(t))
    #     print('\n특정 품사 추출 결과: ')
    #     print(tc_tagger.pos_filter(t, pos=['Noun', 'Hashtag_Noun', 'Emoji']))