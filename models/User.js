const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost:27017/prova_banco', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => {
  console.log('Conexao com o MongoDB estabelecida com sucesso');
}).catch(err => {
  console.error('Erro ao conectar-se ao MongoDB:', err);
});

const userSchema = new mongoose.Schema({
    name: {
      type: String,
      required: true,
      unique: true
    },
    email: {
      type: String,
      required: true
    },
    password: {
      type: String,
      required: true
    }
  }, { collection: 'User' }); 
  
  const User = mongoose.model('User', userSchema);
  
  module.exports = User;
