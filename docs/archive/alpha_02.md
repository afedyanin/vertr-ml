# alpha

## Hands-On Deep Learning for Finance

- Index Replication by Autoencoders
- Volatility Forecasting by LSTM
- Trading Rule Identification by CNN
- Asset Allocation by LSTM over a CNN
- Digesting News Using NLP with BLSTM
- Risk Measurement Using GAN
- Chart Visual Analysis by Transfer Learning
- Training Trader Robots Using Deep Reinforcement Learning

## Quantitative Trading Strategies Using Python

- Trend-Following Strategy
- Momentum Trading Strategy
- Statistical Arbitrage with Hypothesis Testing
- Optimizing Trading Strategies with Bayesian Optimization
- Pairs Trading Using Machine Learning


## Jansen
- Univariate regression – predicting the S&P 500
- Stacked LSTM – predicting price moves and returns
- Multivariate time-series regression for macro data
- LSTM with embeddings for sentiment classification
- Predicting returns from SEC filing embeddings
- A conditional autoencoder for trading
- TimeGAN for synthetic financial data

### Key factor categories

- Momentum and sentiment – the trend is your friend
- Value factors – hunting fundamental bargains
    - Relative value strategies (StatArb)
    - Fundamental value strategies
    - Market value strategies
    - Cross-asset relative value strategies
- Volatility and size anomalies
- Quality factors for quantitative investing

## Машинное обучение: алгоритмы для бизнеса

Полезные финансовые признаки 

### Структурные сдвиги

Структурный сдвиг (structural break), или изменение, или разрыв, представляет собой неожиданный сдвиг во временном ряде, который может привести к огромным ошибкам предсказания и ненадежности модели в целом.
Например, закономерность возвращения к среднему значению может смениться импульсной закономерностью. Когда этот переход происходит, большинство участников рынка оказываются застигнутыми врасплох и будут делать дорогостоящие ошибки.

- Проверки на основе фильтра CUSUM
- Проверки взрываемости
- Суб- и супермартингейловые проверки

### Энтропийные признаки

При несовершенстве рынков цены формируются с частичной информацией, и поскольку некоторые агенты знают больше других, то могут эксплуатировать эту информационную асимметрию.
Например, алгоритм МО может обнаружить, что импульсные ставки выгоднее, когда цены несут мало информации, и что ставки на возврате к среднему значению выгоднее, когда цены несут много информации.

- Энтропия Шеннона
- Подстановочный (или максимально правдоподобный) оценщик
- Оценщики на основе алгоритма LZ
- Схемы кодирования
- Энтропия гауссова процесса
- Энтропия и обобщенное среднее

#### Несколько финансовых приложений энтропии

- Рыночная эффективность
Энтропия ценовой цепочки говорит нам о степени эффективности рынка в данный момент времени. 
«Разжатый» рынок является эффективным рынком, поскольку ценовая информация не избыточна. 
«Сжатый» рынок является неэффективным рынком, поскольку ценовая информация избыточна. Пузыри образуются на сжатых (низкоэнтропийных) рынках.

- Генерирование максимальной энтропии
- Концентрация портфеля
- Микроструктура рынка

### Микроструктурные сдвиги

#### Первое поколение: ценовые последовательности

- Тиковое правило
- Модель Ролла
- Оценщик волатильности максимум-минимум
- Корвин и Шульц

#### Второе поколение: стратегические модели сделок

Они объясняют торговлю как стратегическое взаимодействие между информированными и неинформированными трейдерами. 
При этом они обращают внимание на ориентированный (по знаку) объем и несбалансированность потока ордеров. 

- Лямбда Кайла
- Лямбда Амихуда
- Лямбда Хасбрука

#### Третье поколение: модели последовательных сделок

- Вероятность информационно обусловленной торговли
- Объемно-синхронизированная вероятность информированной торговли


#### Дополнительные признаки из микроструктурных совокупностей данных

- Распределение объемов ордеров
- Скорости отмены, лимитные и рыночные ордера
- Исполнительные алгоритмы TWAP
- Опционные рынки
- Внутрирядовая корреляция ориентированного (по знаку) потока ордеров


