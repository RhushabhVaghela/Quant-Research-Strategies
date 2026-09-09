# Trading Using LLM — Concept Inventory
Exhaustive per-module / per-lesson inventory of every concept taught in this "Trade FOMC meeting using LLM" course, extracted from all notebooks (markdown + code) and the supporting `finbert_sa.py` / `trade_fed_utils.py` modules.
## COURSE: Trading Using LLM
Scope: collect & preprocess FOMC (Fed) press-conference transcripts and SPY price data, score the text with FinBERT (a financial LLM), optionally transcribe earnings-call audio with OpenAI Whisper, then build and compare multiple FOMC sentiment-driven trading strategies via backtesting.
---
## MODULE: Data Collection and Preprocessing
### LESSON: Data Collection and Preprocessing.ipynb
- **FOMC press conference:** post-meeting press conference where the Fed Chair reads a statement — its speech text is the raw sentiment input. prereqs: Federal Reserve, monetary policy
- **FOMC transcripts (PDF):** 21 press-conference transcript PDFs (Jan 2022 – Jul 2024) downloaded from the Federal Reserve website. prereqs: PDFs, data collection
- **FOMC_Timestamp metadata:** CSV of Meeting Date, Start Time, End Time, and Duration of the Chairman's speech per meeting. prereqs: CSV, datetime
- **PDF text extraction (pypdf):** `from pypdf import PdfReader` + `reader.pages[i].extract_text()` to pull text out of each PDF page. prereqs: PDFs, Python
- **Header/footer filtering:** `is_header_or_footer` drops boilerplate lines ("Transcript of Chair Powell's FOMC Press Conference", "Page", "PRELIMINARY") so only speech content remains. prereqs: string matching, data cleaning
- **Speech boundary detection:** locate the start ("Good afternoon.") and end ("Thank you.") phrases to slice out just the Chair's prepared speech. prereqs: substring search, slicing
- **Text cleaning with regex:** `re.sub` fixes broken words/newlines (`\n(?!\s*[A-Z])`), collapses whitespace (`\s+`), and removes spaces before punctuation. prereqs: regular expressions, whitespace
- **Words-per-minute estimation:** total words ÷ speech duration (minutes) so text can be spread evenly across 1-minute bins. prereqs: division, durations
- **Minute-level segmentation:** assign `total_minutes` buckets of ~words_per_minute words each, each tagged with a 1-min timestamp and a `video_id`. prereqs: loops, slicing, datetime
- **Timezone conversion:** `tz_localize('America/New_York').tz_convert('UTC')` turns meeting time into coordinated UTC. prereqs: timezones, pandas
- **Alpaca API for live prices:** `StockHistoricalDataClient(api_key, secret_key)` provides minute-level market data. prereqs: API clients, market data
- **StockBarsRequest / TimeFrame.Minute:** Alpaca request object specifying symbol (SPY), 1-minute timeframe, and start/end for `get_stock_bars`. prereqs: Alpaca API, OHLC
- **OHLC data:** Open/High/Low/Close bars fetched per timestamp for the SPY ETF during the live meeting. prereqs: OHLC, ETFs
- **Data merging:** `pd.merge(result_df, ohlc_df, on='timestamp')` joins speech text with matching price bars. prereqs: DataFrame merge, key column
- **Persisting combined dataset:** save the merged text + OHLC frame to `fomc_text_spy_ohlc_jan22_to_jul24.csv` for sentiment work. prereqs: CSV export
---
## MODULE: Sentiment Analysis of FOMC Transcripts
### LESSON: Sentiment Score of FOMC Transcripts.ipynb
- **FinBERT:** a BERT variant fine-tuned on financial text (earnings calls, analyst reports, financial news) for domain sentiment analysis (positive/negative/neutral). prereqs: BERT, sentiment analysis
- **Load a pre-trained financial LLM:** `finbert_sa.load_model()` loads `ProsusAI/finbert` via `AutoModelForSequenceClassification`. prereqs: transformers, model loading
- **Per-text sentiment scoring:** `finbert_sa.predict_overall_sentiment(text, model)` tokenizes, runs the model, and returns an overall sentiment score. prereqs: FinBERT, inference
- **Batch sentence scoring:** `finbert_sa.process_sentences(model, sentences)` computes a score for each sentence in the FOMC transcript column. prereqs: FinBERT, loops
- **sentiment_score feature column:** store per-minute transcript sentiment scores in the DataFrame for strategy use. prereqs: DataFrame, feature engineering
- **Tokenization & attention features:** internally text is tokenized into `[CLS] ... [SEP]` sequences with `input_ids`, `attention_mask`, `token_type_ids`, zero-padded to fixed length. prereqs: tokenization, transformers
- **Model inference → logits → softmax:** feed tensors through the model under `torch.no_grad()` and convert logits to probabilities with softmax. prereqs: neural inference, softmax
- **Sentiment score from probabilities:** `sentiment_score = logits[:, 0] − logits[:, 1]` (positive-class minus negative-class probability) captures strength, not just label. prereqs: probabilities, arrays
- **Positive / negative / neutral labels:** `argmax` over the 3-class output maps each sentence to a sentiment label dictionary. prereqs: classification, argmax
- **Persisting scored data:** save the frame with scores to `fomc_sentiment_score_spy_ohlc_jan22_to_jul24.csv`. prereqs: CSV export
---
## MODULE: Sentiment Analysis Using Audio Data
### LESSON: Speech to Text.ipynb
- **Speech-to-text / transcription:** converting spoken audio into written text so it can be fed to sentiment models. prereqs: audio, text
- **OpenAI Whisper:** a powerful open speech-recognition model for transcribing audio. prereqs: ASR, audio files
- **Audio model sizes:** `tiny`, `base`, `small`, `medium`, `large` — bigger = more accurate but more compute; here `base` balances accuracy/performance. prereqs: model scale, compute
- **Loading a Whisper model:** `whisper.load_model("base")` downloads/loads the pretrained weights. prereqs: whisper, model loading
- **Transcribing a file:** `model.transcribe(audio_file_name)` (e.g. `amazon_earnings_call_q2_2024.wav`) returns a dict; `result['text']` holds the transcript. prereqs: whisper, .wav/audio
- **Supported audio formats:** m4a, mp3, webm, mp4, mpga, wav, mpeg — convert unsupported files first. prereqs: audio codecs
- **Transcript → sentiment workflow:** the generated earnings-call transcript feeds into FinBERT sentiment analysis. prereqs: transcription, FinBERT
---
## MODULE: Trade FOMC Meeting Using Sentiment Score
### LESSON: Trading Strategy Based on Sentiment Score Threshold.ipynb
- **Rolling / expanding sentiment score:** `video['sentiment_score'].expanding().mean()` accumulates the running mean of minute-level scores up to the current minute. prereqs: pandas expanding, mean
- **Sentiment score threshold:** use `sentiment_score_threshold = 0.1`; long when the rolling score exceeds +0.1, short when below −0.1. prereqs: thresholds, sentiment signals
- **Position state tracking:** `current_position` = 1 (long), −1 (short), 0 (flat) drives the event loop. prereqs: state variables
- **Entry rules:** open long/short when flat and the rolling score crosses the threshold; skip entry on the final minute. prereqs: conditional logic, trading
- **Exit rules:** close a held position when the opposite threshold is crossed or at the meeting's last minute. prereqs: exit logic, event handling
- **trade_sheet ledger:** records Position, Entry Datetime, Entry Price, Exit Datetime, Exit Price per trade. prereqs: tabular data, trade recording
- **Trade P&L:** `pnl = Position × (Exit Price − Entry Price)` yields per-trade profit/loss. prereqs: arithmetic, position sizing
- **Trade-level analytics (`trade_analytics`):** total PnL, number of trades, winners/losers, win & loss %, average PnL per winner/loser, average holding time. prereqs: statistics, trades
- **Signal column update (`update_signal_column`):** copies each trade's position onto the full minute-level SPY series between entry and exit timestamps. prereqs: datetime range slicing, signals
- **Strategy returns:** `strategy_returns = signal.shift(1) × close.pct_change()` (lagged signal × price returns). prereqs: pct_change, lag, returns
- **Equity curve / cumulative returns:** `(strategy_returns + 1).cumprod()` plotted. prereqs: compounding
- **CAGR:** compound annual growth rate annualized from cumulative returns and trading-candle count. prereqs: annualization, growth rate
- **Sharpe ratio:** annualized `(mean strategy return − daily risk-free) / std × sqrt(days)`, risk-free 2%. prereqs: Sharpe, risk-free rate
- **Maximum drawdown:** deepest peak-to-trough decline of the equity curve, plotted and reported. prereqs: equity curve, drawdown
- **Backtesting:** replaying historical sentiment vs price to evaluate a strategy's performance (here Sharpe ≈ 0.96, max DD ≈ 1.08%). prereqs: strategy, performance metrics
---
## MODULE: Strategy Variations to Trade the FOMC Meeting
### LESSON: Trading Strategy With Sentiment Score and Price Trend.ipynb
- **Price trend via moving averages:** `minute_data.close.rolling(window=9).mean()` → `mva9` (short) and window 21 → `mva21` (long). prereqs: moving average, pandas rolling
- **Trend condition:** `mva9 > mva21` signals an upward trend, `mva9 < mva21` a downward trend. prereqs: moving averages, trend
- **Combined sentiment + trend entry:** long only when rolling sentiment > 0.1 AND `mva9 > mva21`; short when rolling sentiment < −0.1 AND `mva9 < mva21`. prereqs: AND logic, sentiment signals, moving averages
- **Combined exit:** opposite thresholds with opposite trend, or last meeting minute. prereqs: exit logic, combined conditions
- **Backtest + analytics:** same `trade_analytics`, `update_signal_column`, `get_performance_metrics` flow (net PnL negative, Sharpe ≈ −2.33). prereqs: backtesting, performance metrics
### LESSON: Trading Strategy Post FOMC Meeting and Price Trend.ipynb
- **Post-report entry:** enter only after the entire FOMC report is released, not during the live meeting. prereqs: event timing
- **Daily FOMC sentiment score:** `daily_sentiment_score_FOMC_Transcript.csv` holds one sentiment score per full report. prereqs: sentiment score, daily aggregation
- **Sentiment + trend post-report strategy:** long when report sentiment > 0 AND `mva9 > mva21`; short when sentiment < 0 AND `mva9 < mva21`. prereqs: moving averages, sentiment threshold
- **End-of-day (EOD) exit:** positions held until the day's last minute bar (`minute_data.loc[str(i)[:10]][-2:-1]`). prereqs: intraday bars, EOD
- **Trade analytics & performance:** same functions; Sharpe ≈ −4.75, max DD ≈ 6.03% — no improvement over the live strategy. prereqs: trade analytics, performance metrics
### LESSON: Trading Strategy Entry Post Report.ipynb
- **Sentiment-only post-report entry:** long when the daily report sentiment > 0, short when < 0, regardless of price trend. prereqs: sentiment score, threshold
- **EOD holding:** enter immediately after the report, exit at the last candle of the day. prereqs: intraday bars, EOD
- **Total pnl / winners / losers:** trade analytics on the sentiment-only variant (Total pnl ≈ 5.08, Win 55.56%). prereqs: trade analytics
- **Performance metrics:** Sharpe ≈ 0.35, max DD ≈ 8.23% — still no improvement vs including the price trend. prereqs: backtesting metrics
### LESSON: Trading Strategy Based on Rolling Text.ipynb
- **Rolling text construction:** `fomc_data.groupby(by_date)['text'].apply(lambda x: x.apply(lambda y: y+' ').cumsum().str.strip())` accumulates all transcript text spoken up to each minute. prereqs: groupby, cumsum, string concat
- **Sentiment of rolling text:** run `finbert_sa.process_sentences` on the `text_rolling` column to get `rolling_sentiment_score` from the cumulative transcript. prereqs: FinBERT, rolling text
- **Rolling-text threshold strategy:** long when rolling text sentiment > 0.1, short when < −0.1; positions closed / not opened at the last minute. prereqs: thresholds, sentiment signals
- **Trade & performance analytics:** same helpers; Sharpe ≈ 0.32, max DD ≈ 1.11% — slightly worse than the rolling-score variant. prereqs: trade analytics, performance metrics
- **Comparison across variants:** rolling-score threshold (best), rolling-text, price-trend combos, and post-report EOD variants are contrasted to see what improves performance. prereqs: backtesting, comparative analysis
---
## MODULE: data_modules (Supporting Code)
### LESSON: finbert_sa.py
- **FinBERT loading helper:** `load_model()` returns `AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert', num_labels=3)`. prereqs: transformers, FinBERT
- **AutoTokenizer:** `AutoTokenizer.from_pretrained('bert-base-uncased')` encodes text to token IDs for the model. prereqs: tokenizers, BERT
- **Sentence tokenization (nltk):** `sent_tokenize` splits text into sentences, each scored independently. prereqs: nltk, sentence segmentation
- **Batching:** a `chunks(l, n)` generator processes sentences in small batches for efficient inference. prereqs: generators, batching
- **convert_examples_to_features:** tokenize → add `[CLS]`/`[SEP]` → `input_ids`, `attention_mask`, `token_type_ids` → zero-pad to `max_seq_length`. prereqs: tokenization, padding
- **softmax over logits:** converts the model's raw 3-class outputs into probabilities. prereqs: softmax, logits
- **Sentiment score = pos-minus-neg probability:** `logits[:,0] − logits[:,1]` gives a continuous score instead of a hard label. prereqs: probability arrays
- **predict_overall_sentiment:** mean of per-sentence scores = the text's overall sentiment score. prereqs: mean, sentence scores
- **process_sentences:** vectorized scoring of full series with a progress bar via tqdm. prereqs: loops, numpy, tqdm
### LESSON: trade_fed_utils.py
- **trade_analytics:** computes total PnL, trade count, winners/losers, win & loss %, average per-trade PnL, and average holding time from a `trade_sheet`. prereqs: statistics, trades
- **update_signal_column:** maps each trade's entry/exit window and position onto a minute-level signal column. prereqs: datetime slicing, signal mapping
- **get_performance_metrics:** returns equity curve, CAGR, Sharpe ratio, and maximum drawdown, with drawdown filling. prereqs: performance metrics, drawdown, Sharpe