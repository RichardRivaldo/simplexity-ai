# Simplexity Board Game

## 📖  How to Run

1. Install virtualenv if you haven't
```
pip install virtualenv
```
2. Create virtualenv
```
virtualenv venv
```

3. Activate the created virtualenv
```
venv\Scripts\activate
```

4. Install dependencies
```
pip install -r requirements.txt
```

5. Run
```
run.bat
```

## How to Play with Others
1. You need to copy class from others to ```minimax.py``` or ```local_search.py``` (for example ```MinimaxA``` and ```MinimaxB``` to ```minimax.py```)
2. Both of them need to have different class name (for example class MinimaxA and class MinimaxB)
3. Run using ```--is_dump``` with bot name define in ```--bot1``` or ```--bot2```

## ⚙️ Config
You can change the config in run.bat
```
 --row <int>
 --column <int>
 --type <bvb?pvb?pvp>
 --player_choice <0?1>
 --thinking_time <float>
 --is_dump
 --bot1 <str>
 --bot2 <str>
```

## ✔️ Acknowledgement
This project is used for an assignment from IF3170 Artificial Intelligence 2021/2022