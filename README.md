# tc_tagger

- tc-tagger의 목적은 인스타그램 텍스트의 특징에 맞는 한국어 자연어처리 패키지를 만드는 것입니다.
- 인스타그램 텍스트는 다른 텍스트와 비교했을 때에 아래와 같은 특징을 가집니다.
    1. 사용자가 본인의 정서를 표현하기 위해 이모지를 빈번하게 사용합니다.
    2. 사용자가 해시태그를 통해 강조하고 싶은 내용이나 공유하고 싶은 내용을 표시합니다.
    3. 신조어를 많이 사용합니다. 사회 전반적인 신조어부터 인스타그램에서만 활용하는 신조어(ex. 좋반, 첫줄반 등)들이 등장합니다.
    4. 다른 텍스트에서 문장부호를 활용하는 방식과는 다른 방식으로 문장부호를 많이 활용합니다. 문장의 종결이 아니라 본인의 정서적 태도를 드러내기 위해 활용하는 경우가 많습니다. 특히 문장부호를 연쇄시켜서 활용하는 경우(ex. '~~~!!!', '.....?') 등이 많습니다.  
- 그러나 기존 형태소 분석기들을 인스타그램 텍스트의 이러한 특징을 잘 반영하지 못하고 아래와 같은 제한 사항들이 발생합니다.
    1. 이모지를 처리하는 태그가 따로 존재하지 않기 때문에 이모지 정보를 활용하기 힘듭니다.
    2. 해쉬태그 표시를 단순하게 하나의 부호로 처리하거나 해쉬태그 뒤의 텍스트를 아예 분석하지  않습니다.
    3. 인스타그램 신조어를 잘 처리하지 못합니다.
    4. 문장부호 여러 개가 조합되어 하나의 의미를 가지는 단위가 되어도 이를 하나하나 나누어서 분석합니다.
- 따라서 tc-tagger는 위의 제한 사항들을 해결하여 인스타그램 텍스트로부터 최대한의 정보를 뽑아낼 수 있으면서도 사용자들이 활용하기 편리한 인스타그램 특화 형태소 분석기를 만드는 것을 목적으로 합니다.

## Guideline

### Install

```powershell
$ git clone https://github.com/HyeonminNam/tc_tagger.git
```

### Python

- 본 패키지는 Python 3.7 버전을 기반으로 구현하였습니다.
- Python 3.x 버전 이상 환경에서 활용하시기를 권장합니다.

### Requires

- 본 패키지를 활용하기 위해서는 사용자 환경에 따라 다음과 같은 패키지들이 필요합니다.
    - 공통
        - 인스타그램 텍스트의 이모지를 처리하기 위한 패키지입니다.

        ```powershell
        $ pip install emoji
        ```

    - 환경별(윈도우, 우분투, 맥 OS)
        - 본 패키지는 Konlpy의 클래스 중 하나인 Okt를 기반으로 만들어졌습니다.
        - 따라서 Konlpy 설치에 필요한 패키지들을 먼저 설치해 주셔야 합니다.
        - 각 환경별로 아래와 같은 패키지가 필요합니다.

            ![github_table](https://user-images.githubusercontent.com/62092003/93077151-61e9f680-f6c3-11ea-9ce3-65fe07a8d361.png)

        - 자세한 설치 방법은 Konlpy 설치 안내 링크([https://konlpy.org/ko/latest/install/](https://konlpy.org/ko/latest/install/))를 참고하시기 바랍니다.

### Docker

- 본 패키지를 설치 및 활용할 수 있는 환경이 갖추어진 Docker 컨테이너를 제공합니다.
- 아래 코드를 실행하시면 미리 구축하여 놓은 Docker 컨테이너에 접근하실 수 있습니다(혹은 github에 업로드한 Docker 이미지를 활용하셔서 직접 빌드하셔도 됩니다).

    ```powershell
    $ docker pull wdg3938/tc_tagger:v1
    $ docker run -it --rm wdg3938/tc_tagger:v1 bash
    $ git clone https://github.com/HyeonminNam/tc_tagger.git
    ```

## Usage

tc-tagger는 Preprocessing(전처리 클래스), Tagger(형태소 분석 클래스)로 구성되어 있습니다.

### Preprocessing

```python
from tc_tagger.TC_preprocessing import Preprocessing
preprocessing = Preprocessing()
```

- tc_tagger의 Preprocessing 클래스는 아래와 같은 전처리 함수들을 제공합니다.
    - extract_hashtag(text)
    - extract_tagged_userID(text)
    - extract_post(text)
    - preprocess_text(text_list, sub_hash=False)

- Preprocessing 클래스는 인스타그램 텍스트에 특화된 전처리 기능을 가지고 있습니다.
    - 텍스트에서 #단어 형식의 해시태그만을 추출 할 수 있습니다.
    - 텍스트에서 @사용자ID 형식으로 태그된 사용자ID를 추출할 수 있습니다.
    - 텍스트에서 해시태그와 사용자ID를 제외한 순수 게시글만 추출할 수 있습니다.
    - 여러 텍스트들에서 한번에 포스트 내용과 해시태그를 분리하여 각각의 리스트로 만들어줄 수 있습니다.

- extract_hashtag(text)의 사용 예시

    ```python
    from tc_tagger.TC_preprocessing import Preprocessing
    preprocessing = Preprocessing()
    text = '다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt'
    preprocessing.extract_hashtag(text)
    ```

    - extract_hashtag 함수는 입력받은 텍스트에 포함된 해시태그를 추출합니다.

    ```python
    #출력값
    ['#멋짐휘트니스연산점', '#연산동pt']
    ```

    - 텍스트에 포함된 해시태그들이 각각 리스트 형식의 안으로 들어간 것을 확인할 수 있습니다.

- extract_tagged_userID(text)의 사용 예시

    ```python
    from tc_tagger.TC_preprocessing import Preprocessing
    preprocessing = Preprocessing()
    text = '앞으로도 좋은 활동 부탁해!!😍😍 @baqq12 @hawp1200'
    preprocessing.extract_tagged_userID(text)
    ```

    - extract_tagged_userID 함수는 텍스트에 태그된 사용자ID를 추출합니다.

    ```python
    #출력값
    ['baqq12', 'hawp1200']
    ```

    - 텍스트에 태그된 사용자ID들이 각각 리스트 형식의 안으로 들어간 것을 확인할 수 있습니다.

- extract_post(text)의 사용 예시

    ```python
    from tc_tagger.TC_preprocessing import Preprocessing
    preprocessing = Preprocessing()
    text = '다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt'
    preprocessing.extract_post(text)
    ```

    - extract_post 함수는 텍스트에서 해시태그와 사용자ID를 제거하고, /n /r /t 등과 같은 공백 문자를 띄어쓰기와 같은 한칸의 공백으로 처리해줍니다.

    ```python
    #출력값
    다이어트 해야되는데...😂😂 . . .
    ```

    - 텍스트에서 순수한 포스트 글만 추출된 것을 확인할 수 있습니다.

- preprocess_text(text_list, sub_hash=False)의 사용 예시

    ```python
    from tc_tagger.TC_preprocessing import Preprocessing
    preprocessing = Preprocessing()
    text_list = ['다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt',
    '럽스타 그자체❤❤ #럽스타그램 #운동하는커플 #연산동pt']
    post_list, hashtag_list = preprocessing.preprocess_text(text_list)
    print(post_list)
    print(hashtag_list)
    ```

    - preprocess_text 함수는 여러 텍스트를 리스트 형식으로 받아 포스트 글 리스트와 해시태그 리스트로 반환해줄 수 있습니다.

    ```python
    #출력값
    ['다이어트 해야되는데...😂😂 . . .  ', '럽스타 그자체❤❤   ']
    [['#멋짐휘트니스연산점', '#연산동pt'], ['#럽스타그램', '#운동하는커플', '#연산동pt']]
    ```

    - 각각의 텍스트의 순수 포스트 글과 해시태그가 리스트 형식으로 추출된 것을 확인할 수 있습니다. 대량의 텍스트 데이터를 전처리하기 용이합니다. 또한 preprocess_text(text_list, sub_hash=False)의 sub_hash를 True로 조정하여 해시태그의 #을 제거하고 추출할 수 있습니다.

### Tagger

```python
from tc_tagger.TC_tagger import Tagger
tagger = Tagger()
```

- tc_tagger의 Tagger 클래스는 아래와 같은 함수들을 제공합니다.
    - tag(text) : 형태소 분석 함수
    - tokenizer(text) : 토큰화 함수
    - pos_filter(text, pos) : 특정 품사 추출 함수

- Tagger 클래스는 아래와 같은 특징을 가지고 있습니다.
    - 이모티콘에 대한 독립된 태그('Emoji')를 제공합니다.
    - 해시태그 뒤의 단어들은 형태소 분석과 더불어서 해시태그 정보임을 보여주는 태그를 붙여줍니다. ex) 'Hashtag_Noun', 'Hashtag_Verb'
    - 인스타그램에 자주 등장하는 신조어가 등록된 사전을 활용합니다.
    - 연속된 문장부호를 하나의 단위로 처리합니다.

- tag(text) 함수 사용 예시

    ```python
    from tc_tagger.TC_tagger import Tagger
    tagger = Tagger()
    text = '럽스타 그자체...❤❤ #럽스타그램 #운동하는커플 #태닝'
    tagger.tag(text)
    ```

    - tag 함수는 입력받은 텍스트에 대해서 형태소 분석을 수행합니다.

    ```python
    # 출력값
    [('럽스타', 'Noun'), ('그', 'Determiner'), ('자체', 'Noun'), ('...', 'Punctuation'), ('❤_red_heart', 'Emoji'), ('❤_red_heart', 'Emoji'), ('럽스타그램', 'Hashtag_Noun'), 
    ('운동', 'Hashtag_Noun'), ('하는', 'Hashtag_Verb'), ('커플', 'Hashtag_Noun'), ('태닝', 'Hashtag_Noun')]
    ```

    - 이모티콘은 각각이 모두 'Emoji'로 태깅되었음을 알 수 있습니다. 또한 이모지의 영문명이 이모지와 함께 부착되어 나타났음('❤_red_heart', 'Emoji')을 확인할 수 있습니다.
    - '럽스타'라는 인스타그램에서 자주 활용되는 신조어가 잘 분석되는 것을 확인할 수 있습니다.
    - 해시태그 뒤의 단어들에도 형태소 분석이 이루어지며 더불어서 해시태그 정보임을 보여주는 태그를 붙어서 나타남을 알 수 있습니다. ex) 'Hashtag_Noun', 'Hashtag_Verb'
    - 연속된 문장부호('...')도 하나의 문장부호로 처리됨을 확인할 수 있습니다.

- tokenizer(text) 함수 사용 예시

    ```python
    from tc_tagger.TC_tagger import Tagger
    tagger = Tagger()
    text = '럽스타 그자체...❤❤ #럽스타그램 #운동하는커플 #태닝'
    tagger.tokenizer(text)
    ```

    - tokenizer 함수는 텍스트를 토큰 단위로 나누는 함수입니다.

    ```python
    # 출력값
    ['럽스타', '그', '자체', '...', '❤_red_heart', '❤_red_heart', '럽스타그램', '운동', '하는', '커플', '태닝']
    ```

    - 텍스트가 토큰별로 잘 나뉘어서 출력된 것을 확인할 수 있습니다.

- pos_filter(text, pos) 함수 사용 예시

    ```python
    from tc_tagger.TC_tagger import Tagger
    tagger = Tagger()
    text = '럽스타 그자체...❤❤ #럽스타그램 #운동하는커플 #태닝'
    tagger.pos_filter(text, pos=['Noun', 'Hashtag_Noun'])
    ```

    - pos_filter 함수는 원하는 품사의 토큰들만 추출할 수 있는 함수입니다.
    - 위 사용 예시에서는 'Noun', 'Hashtag_Noun' 품사를 지정하여 명사들만을 추출하였습니다.

    ```python
    # 출력값
    ['럽스타', '자체', '럽스타그램', '운동', '커플', '태닝']
    ```

    - 출력값을 확인하면 텍스트에서 명사 토큰들만 추출된 것을 확인할 수 있습니다.
