from pymongo import collection
from pprint import pprint

def get_database(db):
    import pymongo
    #return pymongo.MongoClient(f"mongodb+srv://sherensberk:5V*wj$QxbcvXrpGT@cluster0.diykb.mongodb.net/{db}?retryWrites=true&w=majority")[db]
    return pymongo.MongoClient(f"mongodb://omnis:omnis@localhost:37018/{db}", connect=True)[db]
    
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    
    # Get the database
    Omnis = get_database('omnis')
    print(Omnis['camerasteste'].find_one())
    # c = Omnis.test
    # musica = {
    #           "nome": "Nothing left to say",
    #           "banda": "Imagine Dragons",
    #           "categorias": ["indie", "rock"],
    #           "lancamento": "datetime.datetime.now()"
    #          }
    # c.insert_one(musica).inserted_id
    # print(c.find_one())
    # # collection = Omnis['cameras']
    # # for n in collection.find():
    # #     pprint(n)
