# データ構造：既存のデータがあるなら起動前にいじっておく
recruitment = {}
# {person: [{want:str, num:int, active:bool}]}
transaction = {}
# {transaction-number: {person-from:str, person-to:str, card:str, num:int, active:bool}}