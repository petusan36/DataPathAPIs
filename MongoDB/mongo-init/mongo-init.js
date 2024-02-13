conn = new Mongo();
db = conn.getDB("billboard_movie");

db.counters.insert(
   {
      _id: "userid",
      seq: 0
   }
)

function getNextSequence(name) {
   var ret = db.counters.findAndModify(
          {
            query: { _id: name },
            update: { $inc: { seq: 1 } },
            new: true
          }
   );

   return ret.seq;
}

db.createUser(
  {
    user: "pts",
    pwd: "pts12345",
    roles: [
      {
        role: "readWrite",
        db: "billboard_movie"
      }
    ]
  }
);

db.createCollection('my_movies');

db.my_movies.insertOne(
    {
      _id: getNextSequence("userid"),
      autor: "Quentin Tarantino",
      descripcion: "KilBill Vol 1",
      fecha_estreno: "2019-01-01"
    }
);
db.my_movies.insertOne(
    {
      _id: getNextSequence("userid"),
      autor:"Benicio del Toro",
      descripcion:"El extraño mundo de jack",
      fecha_estreno:"2000-12-31"
    }
);