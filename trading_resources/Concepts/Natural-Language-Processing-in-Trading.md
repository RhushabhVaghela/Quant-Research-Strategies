# Natural Language Processing in Trading — Concept Inventory
## COURSE: Natural Language Processing in Trading
Scope: convert financial news headlines into numeric features (BoW, TF-IDF, Word2Vec, BERT), predict sentiment class with XGBoost, aggregate per-day sentiment scores, and build sentiment-based trading strategies on AAPL stocks and bonds. Includes a live-data capstone and news-data collection APIs.
---
## MODULE: Sources of News Headline Data
### LESSON: Sources of News Headline Data.ipynb
- **News headline sentiment dataset:** CSV (`news_headline_sentiments.csv`) containing `news_headline`, `time_stamp`, `URL`, `source_id`, `sentiment_class`, and `sentiment_scores` columns — the raw input for the whole course. prereqs: CSV, pandas DataFrame
- **Chunked CSV reading:** `pd.read_csv(..., chunksize=...)` reads a huge dataset in manageable pieces iterated with a for loop. prereqs: CSV, iterables
- **Data cleaning / drop missing values:** `df.dropna()` removes rows with nulls before filtering. prereqs: DataFrame
- **Lowercasing text:** `df.news_headline.str.lower()` normalizes casing so keyword matching works regardless of case. prereqs: string casing, text preprocessing
- **Keyword filtering by substring:** `df.loc[df.news_headline.str.contains('apple')]` selects only headlines mentioning a target ticker/company. prereqs: boolean masks, regular substring match
- **Data concatenation:** `pd.concat([...])` combines filtered per-chunk dataframes into one full frame. prereqs: two dataframes
- **Word/headline frequency counting:** counting rows per ticker (e.g. aapl/amzn/msft) to gauge data availability. prereqs: `len()` on DataFrame, dict
- **CSV export:** `df.to_csv(...)` persists filtered data (e.g. `news_headline_sentiments_aapl.csv`) for downstream use. prereqs: CSV writing, pandas
---
## MODULE: Bag of Words
### LESSON: Bag of Words Calculation.ipynb
- **Bag of Words (BoW):** the simplest way to convert text into a numeric vector by counting word frequency per document — ignores word order. prereqs: corpus, words
- **Corpus:** a collection of text documents (here a list of sentences) used as input. prereqs: Python list, text
- **Tokenization:** splitting a document into its constituent tokens/words — CountVectorizer does this internally. prereqs: words, text
- **CountVectorizer (sklearn):** `from sklearn.feature_extraction.text import CountVectorizer`; fits a vocabulary and counts occurrences to build a document-term frequency matrix. prereqs: BoW concept
- **fit_transform:** fits the vectorizer on the corpus and transforms it into the count matrix in one call. prereqs: CountVectorizer, fit/transform
- **Feature / vocabulary extraction:** `cv.get_feature_names_out()` returns the learned word features (unique terms). prereqs: CountVectorizer
- **Document-term matrix:** counts laid out as a DataFrame (rows=documents, columns=terms); note `toarray()` converts the sparse output to a dense array. prereqs: sparse matrix, DataFrame
- **Default CountVectorizer preprocessing:** by default everything is lowercased, words < 2 letters are dropped, punctuation is removed, and duplicate tokens are collapsed. prereqs: CountVectorizer, text preprocessing
---
## MODULE: TF-IDF
### LESSON: TF-IDF Calculation.ipynb
- **Term Frequency (TF):** how many times a word appears in a document — same as the BoW count. prereqs: BoW
- **Inverse Document Frequency (IDF):** measures a word's significance; the more documents a word appears in, the less significant it is. prereqs: term frequency, document frequency
- **IDF formula:** `IDF = log(N / df(t))` where N is the number of documents and df(t) the count of documents containing term t. prereqs: logarithms, document frequency
- **Smoothed IDF:** sklearn uses `1 + log(N/df(t))` so terms appearing in every document (IDF=0) are still given weight. prereqs: IDF formula, log
- **TfidfTransformer:** sklearn component that takes a count matrix and re-weights it into TF-IDF values via `fit`/`transform`. prereqs: CountVectorizer output, TF-IDF
- **TfidfVectorizer (direct):** computes TF-IDF from raw text directly (`fit_transform`) instead of counting first. prereqs: TF-IDF, vectorizer
- **TF-IDF product rule:** TF-IDF score = TF × IDF per term. prereqs: TF, IDF
- **stop_words removal:** `stop_words='english'` strips common words (the, and, of...) that carry little meaning. prereqs: tokenization, BoW
- **L1 / L2 normalization:** `norm='l2'` (default) scales each row to unit length; `norm='l1'` scales absolute values to sum to 1 — prevents long documents dominating. prereqs: norm, vector math
- **smooth_idf & use_idf flags:** `smooth_idf=False` uses the unsmoothed IDF; `use_idf=True` enables IDF re-weighting. prereqs: IDF
### LESSON: TF-IDF to XGBoost.ipynb
- **TF-IDF → XGBoost pipeline:** feed TF-IDF vectors into XGBClassifier to predict sentiment, mirroring the BoW workflow. prereqs: TF-IDF, XGBClassifier
- **Sentiment target mapping:** map sentiment labels `{-1,0,1}` → `{0,1,2}` so they fit classifier conventions. prereqs: label encoding, sentiment class
- **Predictor / target variables:** `X` = news headlines, `y` = sentiment_class (dependent variable predicted from independent features). prereqs: ML features/labels
- **train/test split:** split data (80% train / 20% test); use `fit_transform` on train and only `transform` on test (never refit on test). prereqs: overfitting, fit/transform
- **XGBClassifier fit & predict:** `XGBClassifier(max_depth=6, n_estimators=100, eval_metric='mlogloss')` then `.fit()` on train and `.predict()` on test. prereqs: gradient boosting, classification
- **accuracy_score:** fraction of correct predictions on the test set (≈0.709 here). prereqs: classification metrics
---
## MODULE: Predicting Sentiment Score Using XGBoost
### LESSON: BoW to XGBoost.ipynb
- **Sentiment classification task:** predict the sentiment class of a news headline (positive/neutral/negative) — a 3-class supervised classification problem. prereqs: classification, sentiment
- **Target variable y:** `sentiment_class` remapped from `{-1,0,1}` to `{0,1,2}`. prereqs: label encoding
- **Predictor variable X:** the raw `news_headline` strings, coerced to `str`. prereqs: ML feature columns
- **train/test split:** 80/20 ratio; recommended to keep ≥ 60% for training. prereqs: overfitting, holdout
- **Bag-of-Words vectorization with stopwords:** `CountVectorizer(stop_words='english', lowercase=True)`, fit on train, transform on test. prereqs: BoW, stop words
- **XGBClassifier hyperparameters:** `max_depth` (limits tree/node depth) and `n_estimators` (number of boosted trees), `eval_metric='mlogloss'` for multi-class. prereqs: XGBoost, decision trees
- **Model fitting & prediction:** `xg.fit(X_new_train, y_train)` then `xg_model.predict(X_new_test)`. prereqs: XGBClassifier
- **Confusion matrix:** `sklearn.metrics.confusion_matrix` shows true-vs-predicted counts per class for a classification model. prereqs: classification metrics
- **Classification report:** `classification_report` summarizes precision, recall, and F1-score per class. prereqs: precision/recall/F1
- **Prediction accuracy:** `accuracy_score(y_test, prediction)` — ≈0.725 here. prereqs: accuracy metric
---
## MODULE: WordVec
### LESSON: Basic Implementation.ipynb
- **Word embeddings:** dense vector representations of words learned from corpora, where similar words map near each other. prereqs: vectors, text
- **Word2Vec (gensim):** `gensim.models.Word2Vec` learns word vectors from tokenized text (a neural embedding model). prereqs: word embeddings, gensim
- **NLTK tokenization:** `nltk.download('punkt')` + `word_tokenize` split each headline into a list of word tokens. prereqs: tokenization, nltk
- **Tokenized corpus input:** Word2Vec takes a list of lists of words (tokenized sentences) as training input. prereqs: tokenization, Word2Vec
- **min_count parameter:** `Word2Vec(tokens, min_count=2)` keeps only words appearing at least twice in the corpus. prereqs: Word2Vec, corpus frequency
- **Vector dimensionality:** `size=300` sets 300-dimensional word vectors. prereqs: vector dimensions
- **Word similarity:** `word2vec.wv.similarity('United','States')` returns cosine-style similarity between word vectors. prereqs: word vectors, similarity
- **most_similar:** `word2vec.wv.most_similar('Stock')` returns nearest-neighbor words ranked by similarity. prereqs: word vectors, similarity
- **Word vector retrieval:** `word2vec.wv['states']` gives the 300-dim vector for a word. prereqs: word vectors, numpy array
- **Sentence vector:** `word2vec.wv[sentence]` stacks each word's vector into a sentence matrix. prereqs: word vectors, matrices
- **Average sentence vector:** `np.average(np.vstack(sentence_vector), axis=0)` collapses word vectors to one mean vector per sentence. prereqs: numpy, averaging, matrices
- **Data pre-processing for Word2Vec:** sort by timestamp, keep headline+sentiment columns, drop duplicates and missing values. prereqs: pandas, data cleaning
- **Chunked data ingestion:** read the large CSV in 50k-row chunks. prereqs: CSV, pandas chunks
### LESSON: Word2Vec Using Google Model.ipynb
- **Pre-trained Google News Word2Vec:** load Google's large pre-trained model via `gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300-SLIM.bin', binary=True)`. prereqs: Word2Vec, model files
- **KeyedVectors:** gensim class for loading/inspecting pre-trained word vectors without the training model. prereqs: gensim, pre-trained embeddings
- **Pre-trained similarity lookup:** `word2vec.most_similar('Stock')` and `word2vec.similarity('Cat','Australia')` on the Google vocabulary. prereqs: word vectors, similarity
- **Pre-trained word vector:** `word2vec['states']` retrieves the 300-dim vector. prereqs: KeyedVectors
- **Pre-trained sentence vector:** `[word2vec[x] for x in sentence_token]` then average over dimensions (results in a 300-dim vector). prereqs: word vectors, averaging, numpy
### LESSON: Word2Vec to XGBoost.ipynb
- **Embedding averaging function:** `create_vector(words, model, num_features)` sums word vectors present in the model and divides by count to get a headline vector. prereqs: word embeddings, numpy
- **Sentence-to-vector helper:** `create_vector_from_news_headline` builds a matrix of averaged vectors for a whole set of headlines. prereqs: create_vector, matrices
- **Feature/target extraction:** `get_feature_and_target_variable` tokenizes lowercased headlines keeping only in-vocabulary words, then produces X (vectors) and y (class). prereqs: tokenization, word vectors
- **Incremental model training:** feed chunks sequentially, using `xg.fit(X, y, xgb_model=xg.get_booster())` to continue boosting from the previous model — enables training on data larger than memory. prereqs: XGBoost, boosting, chunks
- **XGBClassifier on embeddings:** `XGBClassifier(max_depth=5, n_estimators=20, learning_rate=0.50, eval_metric='mlogloss')`. prereqs: gradient boosting, hyperparameters
- **Class remapping function:** `remap()` converts predicted/actual labels back from `{0,1,2}` to `{-1,0,1}`. prereqs: label encoding
- **Confusion matrix / classification report:** evaluate Word2Vec-based predictions; the model here predicts only the neutral class, showing Word2Vec works poorly on sentences. prereqs: classification metrics
- **Word2Vec limitation:** works well on individual words but not on whole sentences (no context handling) → motivates context-aware BERT. prereqs: Word2Vec, sentence embeddings
---
## MODULE: BERT
### LESSON: Implementation of BERT Model.ipynb
- **BERT (Bidirectional Encoder Representations from Transformers):** a Google NLP model trained bidirectionally so it understands word context (e.g. differentiates "bucket list" from "bucket of water"). prereqs: word embeddings (Word2Vec), transformers
- **BERT training data:** pretrained on Wikipedia (≈2.5B words) + BookCorpus (≈800M words). prereqs: BERT, language models
- **BERT model sizes:** Base (12-layer, 768-hidden, 12-heads, 110M params) vs Large (24-layer, 1024-hidden, 16-heads, 340M params); case-preserved and uncased variants. prereqs: transformer architecture, parameters
- **BERT as a Service:** `from bert_serving.client import BertClient` exposes a running BERT server over a client; `encode()` converts sentences to fixed-length vectors with little code. prereqs: client-server, BERT
- **BERT word embeddings:** `bc.encode(news_headline)` returns a 768-dim vector per sentence (here shape (2, 768)). prereqs: BertClient, embeddings
- **Uncased BERT + context awareness:** encoding news headlines to feed a downstream classifier. prereqs: BERT embeddings, XGBoost
### LESSON: BERT to XGBoost.ipynb
- **BERT-embedding features:** use `BertClient.encode` to produce the feature matrix `X` from the headline column. prereqs: BERT embeddings, feature engineering
- **BERT + XGBoost classifier:** `XGBClassifier(max_depth=5, n_estimators=20, learning_rate=0.50, eval_metric='mlogloss')` trained on BERT vectors. prereqs: XGBClassifier, BERT
- **Incremental training with embeddings:** same `xgb_model=xg.get_booster()` chunked-boosting pattern on BERT vectors. prereqs: incremental training, XGBoost
- **Target remapping:** `y = df[sentiment_column].replace(-1, 2)`. prereqs: label encoding
- **Confusion matrix / classification report:** evaluate the BERT-featured model on the test set. prereqs: classification metrics
---
## MODULE: Sentiment Score and Strategy Logic
### LESSON: Calculate Daily Sentiment Score in Python.ipynb
- **Daily sentiment score:** the mean of `sentiment_class` for all headlines mapped to one trading day — the signal that drives strategies. prereqs: mean, sentiment class
- **Trading time assignment (`get_trade_open`):** maps each headline timestamp to the market-open time when it should be used for trading. prereqs: datetime, market hours
- **Market open/close times:** US session 09:30 open / 16:00 close, used as boundaries for headline bucketing. prereqs: market hours, datetime
- **Business-day offset (BDay):** `from pandas.tseries.offsets import BDay` computes previous/next business/trading days (skipping weekends). prereqs: pandas offsets, trading calendar
- **Previous-day close / next-day open:** computed to decide which day's session a headline belongs to. prereqs: BDay, datetime arithmetic
- **Headline bucketing rule:** headlines made after previous close and before today's open → today's open; after today's close and before next open → next day's open; headlines during market hours are ignored. prereqs: conditional logic, trading sessions
- **Grouped mean aggregation:** `data.groupby('trading_time').sentiment_class.agg('mean')` yields one score per session — "one approach"; more refined scores can ignore weak headlines. prereqs: groupby, aggregation
- **Date normalization:** floor timestamps to day, strip timezone, set Date as index for clean visualization. prereqs: pandas datetime, tz handling
- **Persist score:** `to_csv('apple_daily_sentiment.csv')` for reuse in strategies. prereqs: CSV writing
---
## MODULE: Sentiment Strategy on Stocks
### LESSON: Sentiment Strategy on Stocks.ipynb
- **Sentiment-based trading signals:** a `signal` column where score ≥ 0.25 → buy (1), score ≤ −0.25 → sell (−1), else neutral (0); thresholds are arbitrary/tunable. prereqs: sentiment score, thresholding
- **Data merging:** `aapl_stock_data.merge(sentiment_df, on='Date')` joins daily prices with daily sentiment on matching dates. prereqs: DataFrame merge, key column
- **Open-to-open returns:** `prices['Open'].pct_change()` computes daily returns between consecutive opens. prereqs: returns, prices
- **Signal lagging (avoid lookahead):** `strategy_return = signal.shift(1) * return` trades on yesterday's signal, holding through today's return. prereqs: pandas shift, lookahead bias
- **Cumulative strategy returns:** `(strategy_return + 1).cumprod()` compounds returns to an equity curve. prereqs: compounding, cumulative product
- **Sharpe ratio:** annualized `(mean excess return / std) × sqrt(252)`, using a 2% risk-free rate and 252 trading days → ≈0.88 here. prereqs: risk-free rate, standard deviation, annualization
---
## MODULE: Sentiment Strategy on Bonds
### LESSON: How to Calculate Bond Returns_.ipynb
- **Bond data fields:** bid/ask/mid OAS, bid/ask/mid price and yield, coupon, maturity, duration from an AAPL bond CSV. prereqs: bonds, market data
- **Option-Adjusted Spread (OAS):** measure of the bond's spread over a risk-free benchmark after adjusting for embedded options; `bid_oas`/`ask_oas`/`mid_oas`. prereqs: bond spreads, options
- **Daily OAS change:** `mid_oas.diff()` = today's OAS minus previous day's, used as the driver of bond returns. prereqs: pandas diff, spreads
- **Bond duration:** weighted average time until a bond's cash flows are received; measures price sensitivity to yield changes. prereqs: bond pricing, cash flows
- **Bond return formula:** `bond_returns = (−duration × daily_change_oas) / 100`. prereqs: duration, OAS change
- **Cumulative bond P&L:** `(bond_returns/100 + 1).cumprod()` plotted as daily profit & loss; persist returns to `bond_returns_aapl.csv`. prereqs: compounding, CSV export
### LESSON: Sentiment Strategy on Bonds.ipynb
- **Bond sentiment strategy:** identical logic to the stock strategy but applied to bond returns (long when score > 0.25, short when < −0.25). prereqs: sentiment signals, bond returns
- **Bond return + sentiment merge:** join `bond_returns_aapl.csv` with daily sentiment on Date. prereqs: DataFrame merge
- **Strategy return on bonds:** `strategy_return = signal.shift(1) * bond_returns`. prereqs: pandas shift, returns
- **Cumulative bond strategy plot:** `(strategy_return/100 + 1).cumprod()` visualized as cumulative percentage returns. prereqs: cumulative product, plotting
---
## MODULE: Paper and Live Trading
### LESSON: Recent News Headline Data.ipynb
- **News data APIs:** Webhose, NewsAPI, News Fetch, GoogleNews aggregate headlines; pick one, read its docs. prereqs: APIs, networking
- **API key & client init:** `from newsapi import NewsApiClient; newsapi = NewsApiClient(api_key=...)`; keys from registration. prereqs: API keys, client objects
- **Fetching articles with filters:** `newsapi.get_everything(q=keyword, language='en', sort_by='publishedAt', page_size=...)` filters by keyword, language, recency. prereqs: NewsAPI, query params
- **Article information extraction:** pull Title, description, URL, publication date per article into a DataFrame for downstream sentiment. prereqs: loops, pandas
- **Live-data workflow:** the fetched recent headlines feed into sentiment prediction and strategies in the capstone. prereqs: sentiment prediction, strategy
---
## MODULE: Capstone Project
### LESSON: Model Solution.ipynb
- **End-to-end sentiment pipeline:** read data → choose target/predictor → 80/20 split → Bag of Words → XGBoost train → accuracy. prereqs: BoW, XGBoost, train/test
- **max_features constraint:** `CountVectorizer(..., max_features=200)` limits vocabulary size to 200 terms. prereqs: CountVectorizer, feature dimension
- **XGBoost training & accuracy:** `XGBClassifier(max_depth=6, n_estimators=100)` fit and `accuracy_score` (≈0.5499 on full data). prereqs: XGBClassifier, accuracy
- **Fetching recent news (NewsAPI):** loop keywords/date ranges, `newsapi.get_everything`, dedupe into `article_info`. prereqs: NewsAPI, pandas
- **Predict sentiment on new headlines:** convert to str, `count_vectorizer.transform(...)`, `xg_model.predict(...)`, attach class column. prereqs: vectorizer transform, predict
- **Trading-time assignment for live data:** reuse `get_trade_open` to bucket recent headlines into sessions. prereqs: trading time logic
- **Live daily sentiment score:** groupby trading_time → mean sentiment as before. prereqs: groupby mean
- **Yahoo Finance price fetch:** `yfinance.download('AAPL', start, end)` retrieves daily OHLC. prereqs: yfinance, OHLC
- **Live sentiment trading strategy:** buy when score > 0, sell when score < 0; `returns = Open.pct_change()`, `strategy_returns = signal.shift(1) * returns`, plot cumulative. prereqs: signals, returns, shift
---
## MODULE: data_modules (Supporting Code)
- **BERT server IP helper:** `get_ip_address()` returns the host of the BERT server used by `BertClient`. prereqs: BERT as a Service
- **Tweepy/Twitter API access:** `tweepy.AppAuthHandler` builds a Twitter API client; `tweepy.Cursor(api.search, q=...)` streams tweets by query. prereqs: Twitter API, OAuth
- **Tweet metadata extraction:** `full_text`, `id_str`, `retweet_count`, `created_at`, `user.screen_name` from tweet objects. prereqs: tweepy, data extraction
- **VADER sentiment:** `from vaderSentiment ... SentimentIntensityAnalyzer`; `analyzer.polarity_scores(text)['compound']` produces a compound sentiment score for arbitrary text. prereqs: sentiment analysis, lexicon
- **Date-window querying:** `since`/`until` date strings (today ± 1 day) bound the tweet search window. prereqs: datetime, search queries
- **Reusable extraction functions:** helper functions to fetch tweets by query or by ID list and return a tidy DataFrame. prereqs: functions, pandas
---
## Natural-Language-Processing-in-Trading — Section-based course structure
# — Natural Language Processing in Trading — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs only (no mp4s present).
**Overlap with D: notebooks:** partial — the D: side holds notebook-based NLP-in-trading extraction (news sentiment → strategy). This package mirrors it but deepens the word-embedding method theory (BoW → TF-IDF → Word2Vec → BERT) plus BERT fine-tune/adaptation.
## COURSE
Use news headlines to drive sentiment-based trading strategies: tokenising headlines, converting text to numeric vectors via word-embedding methods (Bag of Words, TF-IDF, Word2Vec, BERT), training an XGBoost/BERT classifier over a labelled sentiment dataset, calculating sentiment class of unseen headlines, fine-tuning/adapting BERT to financial spread-change prediction, comparing embedding methods, and finally paper/live trading (IBridgePy) the model.
## Course Prerequisite Map
- **Section 10 Sentiment Class becomes requires:** pandas / CSV handling, a way to compute features for a classifier.
- **Section 12 WordVec requires:** Section 10 setup + vectorisation concepts (BoW dim+ordering problems, TF-IDF weighting).
- **Section 13 BERT requires:** Sections 10 + 12 (embedding progression) + transformer/attention intuition.
- **Section 14 BERT Adaptation requires:** Section 13 (a pre-trained BERT fine-tuned workflow).
- **Section 15 Result Analysis requires:** Sections 12–14 (all four embedding methods) + comparison / evaluation metrics.
- **Section 18 Paper & Live Trading requires:** Section 15 (a working sentiment model) + news data sources.
- **Section 19 Capstone requires:** all prior + ML classifier construction.
- **Section 20 Summary** requires all.
---
### Section 10 — Sentiment Class of News Headlines
- **CONCEPT:** Sentiment-class label — training set of headlines tagged with a sentiment class (used to train a classifier that labels any new headline). **Train/Test breakout (80/20).** prereqs: pandas, text features.
- **CONCEPT:** Vectorise and classify — tokenise headline, convert to numeric via a word-embedding method, pass vector + class to XGBoost, then test accuracy. prereqs: tokenizer + bag-of-words + a gradient-boosting classifier.
- **CONCEPT:** Build a trading strategy per the sentiment class — once classed, the label drives the strategy (e.g., trade Apple stock on daily-headline sentiment). prereqs: Section 10 classifier + data.
### Section 12 — WordVec
- **CONCEPT:** Limitations of Bag-of-Words (BoW) & TF-IDF — **dimension blow-up** (one dimension per unique word across all documents) and **ordering loss** (BoW loses word order/meaning — "This is Good" vs "Is this Good" same vector); TF-IDF adds word-weighting within a document (frequent + signature words get weight) but still limited. prereqs: vectorisation, text data.
- **CONCEPT:** Word2Vec — overcome BoW/TF-IDF limits by learning **distributed dense vectors** through **two-layer neural networks** with two training tactics: **CBOW** and **Skip-Gram**. The vectors are low-dim and wear meaning (similar words placed nearby in embedding space). prereqs: BoW/TF-IDF limitations + neural net basics.
### Section 13 — BERT
- **CONCEPT:** BERT (Google, 2018) — **Bidirectional Encoder Representations from Transformers**: a transformer trained bidirectionally to learn contextual relation (probability over word/sub-word sequences) — vs sequential left-to-right/right-to-left models. prereqs: word embeddings + encoder/attention.
- **CONCEPT:** Two training strategies — pre-training with masked language modelling + next-sentence prediction, then fine-tuning on a downstream task (e.g. sentiment). prereqs: transformer, fine-tuning.
- **CONCEPT:** BERT setup / deployment — install/use `transformers`, run in Google Colab; pre-trained model weights from Google available. prereqs: programming + tokenizer.
### Section 14 — BERT Model Adaptation
- **CONCEPT:** Fine-tuned BERT baseline — pre-trained BERT fine-tuned on single-firm (Apple) headlines to predict **daily spread changes**; the naive model predicts one-sided (all positive, 51%–52% range) → it captured no real signal, only dataset imbalance. prereqs: Section 13.
- **CONCEPT:** Adapting the last layer — because pre-trained BERT is general-language (on sentiment 3-class it did well → 66%), and re-pre-training is impossible (huge finance corpus/gPU/time), instead **modify the last layers** of BERT and add a flexible task-specific downstream model, using Google's embeddings as a feature extractor. prereqs: Section 13 + transfer learning.
### Section 15 — Result Analysis
- **CONCEPT:** Comparing the four embedding methods — **BoW**: simplest; counts word frequency per doc (loses order). **TF-IDF** better at relevance. **Word2Vec** less polys not ordered, meaning-bearing dense vectors. **BERT** contextual/bidirectional — best of context but heavy. Choose by task/data size and interpretability priorities. prereqs: Sections 12–14.
### Section 18 — Paper and Live Trading
- **CONCEPT:** Sources of news-headline data — `news-fetch` python crawler; **News API** (REST); Google News fetch via Python. prereqs: web data + Section 15.
- **CONCEPT:** Paper/live template — IBridgePy NLP template (`IBridgePyNLP.zip`) to paper/live trade the sentiment model on a broker. prereqs: Section 15 worked model + broker connection.
### Section 19 — Capstone Project
- **CONCEPT:** Capstone — build an end-to-end NLP trading strategy: train embedding + classifier on the headline sentiment data (BoW → XGBoost, template + data files supplied), fetch/apply to your own headlines, define the strategy, backtest/paper/Live. prereqs: all prior.
### Section 20 — Course Summary
- **CONCEPT:** Recap + resources (`Natural-Language-Processing-in-Trading-Resources.zip`) — wraps the full pipeline (headlines → embeddings → classifier → strategy → live). prereqs: entire course.