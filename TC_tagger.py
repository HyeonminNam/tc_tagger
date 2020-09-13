import os
import sys
sys.path.append(os.path.dirname(__file__))
from konlpy_tc.tag import Okt_edit
import emoji
import re
import pandas as pd



class tagger():

    def __init__(self):
        self.emoji_dic = emoji.UNICODE_EMOJI
        self.emoji_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.re_emoji = re.compile('|'.join(re.escape(p) for p in self.emoji_list))
        self.okt_edit = Okt_edit()
        self.re_hashtag = re.compile('')
        
       
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
                token = re.search('[#](\w+)', token).group(1)
                phrase_lst = self.okt_edit.phrases(token)
                if len(phrase_lst) == 0:
                    phrase = token
                else:
                    phrase = phrase_lst[0]
                new_token = re.sub(phrase, ' '+phrase+' ' , token).strip().split()
                h = []
                for x in new_token:
                    if x == phrase:
                        h.append((x, 'Hashtag_Noun'))
                    else:
                        tmp = self.okt_edit.pos(x)
                        for token_, tag_ in tmp:
                            h.append((token_, 'Hashtag_'+tag))         
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
    text3 = '우뤠기 갑자기 \U0001fa78💩 싸고 🤮 하고 왜그래.. 지발로 켄넬들어가서 몸 말고 자고있고. ㅠ 엄마 수업 간 사이 그 좋은 열빙어포도 터키츄도 건드리지도 않고 ㅠ. 걀국 병원와서 혈액검사즁. 아프지마 내새꾸. My boy doesn’t feel well today and finally paid a visit to a local vet for some \U0001fa78 tests done. 😭😭-#billie #puppy #puppystagram #puppylove #puppyson #maltipoo #dog #dogstagram #puppymomlife #mydogismychild #daily #2020 #빌리 #개린이 #말티푸 #개아들 #개스타그램 #강아지 #강아지스타그램 #댕댕이 #멍멍이 #멍뭉이 #뽀시래기 #개집사 #일상 #갱얼쥐 #내새꾸'
    tc_tagger = tagger()
    print(tc_tagger.nouns(text3))
    # for t in [text1, text2, text3]:
    #     print('='*100)
    #     print('\nThreecow : ', tc_tagger.tag(t))
    #     print('\n', '='*100)
    #     print('\ntokenize 결과: ')
    #     print(tc_tagger.tokenizer(t))
    #     print('\nnouns 추출 결과: ')
    #     print(tc_tagger.nouns(t))