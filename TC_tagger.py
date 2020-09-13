import os
import sys
sys.path.append(os.path.dirname(__file__))
from konlpy_tc.tag import Okt_edit
import emoji
import re



class tagger():

    def __init__(self):
        self.emoji_dic = emoji.UNICODE_EMOJI
        self.emoji_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.re_emoji = re.compile('|'.join(re.escape(p) for p in self.emoji_list if p != '\u200d|\u200c'))
        self.okt_edit = Okt_edit()
        self.re_hashtag = re.compile('')
        
       
    def emoticon(self, result):
        emo_lst = []
        for idx, (token, _) in enumerate(result):
            emojis = re.findall(self.re_emoji, token)
            if emojis:
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
                            h.append((token_, 'Hashtag_'+tag_))         
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
    text1 = '다이어트 해야되는데...😂😂 #멋짐휘트니스연산점 #연산동pt'
    text2 = '럽스타 그자체❤❤\n#럽스타그램 #운동하는커플 #태닝'
    text3 = '내가 이사하는 곳은 모르고 왔어도 항상 공사예정. 아님 한국은 항상 공사중인건가. 어쩌다 홍삼투여하고 림프절 내가 막 문대면서 어쩌다 대책위. 스트레스 극취약한 내가 이러면 되겠슴까 안되겠슴까. 🤦🏽\u200d♀️#아파트열사 노인인구가 압도적으로 많은 단지분위기로다가 아무도 무엇에 관심을 두지않아서 지극히 #개인주의 인 내가 이런짓을. '
    tc_tagger = tagger()
    print(tc_tagger.tag(text3))
    # for t in [text1, text2, text3]:
    #     print('='*100)
    #     print('\nThreecow : ', tc_tagger.tag(t))
    #     print('\n', '='*100)
    #     print('\ntokenize 결과: ')
    #     print(tc_tagger.tokenizer(t))
    #     print('\nnouns 추출 결과: ')
    #     print(tc_tagger.nouns(t))