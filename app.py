from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.app_context().push()

class AddressBook(db.Model):
    __tablename__ = "addressbook"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    mobile = db.Column(db.Integer)
    pincode = db.Column(db.Integer)
    _type = db.Column(db.String)
    isPermanent = db.Column(db.Boolean, default=False)
    isBusiness = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            "id":self.id,
            "name":self.name,
            "mobile":self.mobile,
            "pincode":self.pincode,
            "_type":self._type,
            "isPermanent":self.isPermanent,
            "isBusiness":self.isBusiness
        }


db.create_all()


@app.route('/address/', methods=['POST', 'GET'])
def get_and_post():
    if request.method == 'POST':

        # TESTING/LEARNING Purpose only -- Receiving json data
        if request.is_json :
            # incoming data type
            print(request.content_type) # application/json
            name = request.json['name']
            return jsonify({'name':name}), 201

        # incoming data type
        print(request.content_type) # application/x-www-form-urlencoded

        try:
            name = request.form['name']
            mobile = request.form['mobile']
            pincode = request.form['pincode']
            _type = request.form['_type']

            try:
                assert 8<=len(name)<=15
                try:
                    addr = AddressBook.query.filter_by(name=name).first()
                    if addr :
                        raise Exception
                except:
                    return "duplicate name not allowed", 400
            except:
                return "name is invalid", 400

            try:
                assert len(mobile) == 10
                mobile = int(mobile)
            except:
                print(type(mobile))
                return "mobile number is invalid", 400

            try:
                pincode = int(pincode)
                assert 10000<=pincode<=10000000 
            except:
                return "pincode is invalid", 400

            try:
                assert _type in ['permanent', 'business', 'both']
            except:
                return "type is invalid", 400


            # finally add data to database
            addr = AddressBook(name=name, mobile=mobile, pincode=pincode, _type=_type)

            if _type == 'permanent':
                addr.isPermanent = True
            elif _type == 'business':
                addr.isBusiness = True
            elif _type == 'both':
                addr.isBusiness = True
                addr.isPermanent = True

            db.session.add(addr)
            db.session.commit()

            return jsonify(addr.serialize()), 201

        except:
            return "incomplete data passed", 400

    if request.method == 'GET':
        all_addr = AddressBook.query.all()
        res = [addr.serialize() for addr in all_addr]

        return jsonify(res), 200




if __name__ == '__main__':
    app.run(debug=True)
