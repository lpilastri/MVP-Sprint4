/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/fontes';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.fontes.forEach(item => insertList(item.name, 
                                                item.ph, 
                                                item.hard,
                                                item.solid,
                                                item.chlo,
                                                item.sulf,
                                                item.cond,
                                                item.orgcarb,
                                                item.trih,
												                        item.turb,
                                                item.outcome
                                              ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputFonte, inputPh, inputHard,
                        inputSolid, inputChlo, inputCondc,
                        inputSulf, inputOrgn, inputTrih, inputTurb) => {
    
  const formData = new FormData();
  formData.append('name', inputFonte);
  formData.append('ph', inputPh);
  formData.append('hard', inputHard);
  formData.append('solid', inputSolid);
  formData.append('chlo', inputChlo);
  formData.append('sulf', inputSulf);
  formData.append('cond', inputCondc);
  formData.append('orgcarb', inputOrgn);
  formData.append('trih', inputTrih);
  formData.append('turb', inputTurb);

  let url = 'http://127.0.0.1:5000/fonte';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/fonte?name='+item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputFonte = document.getElementById("newInput").value;
  let inputPh = document.getElementById("newPh").value;
  let inputHard = document.getElementById("newHard").value;
  let inputSolid = document.getElementById("newSolid").value;
  let inputChlo = document.getElementById("newChlor").value;
  let inputCondc = document.getElementById("newConduc").value;
  let inputSulf = document.getElementById("newSulf").value;
  let inputOrgn = document.getElementById("newOrgan").value;
  let inputTrih = document.getElementById("newTrih").value;
  let inputTurb = document.getElementById("newTurb").value;

  // Verifique se o nome do produto já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/fontes?nome=${inputFonte}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.fontes && data.fontes.some(item => item.name === inputFonte)) {
        alert("A fonte já está cadastrado.\nCadastre o paciente com um nome diferente ou atualize o existente.");
      } else if (inputFonte === '') {
        alert("O nome da fonte não pode ser vazio!");
      } else if (isNaN(inputPh) || isNaN(inputHard) || isNaN(inputSolid) || isNaN(inputChlo) || isNaN(inputCondc) || isNaN(inputSulf) || isNaN(inputOrgn) || isNaN(inputTrih)) {
        alert("Esse(s) campo(s) precisam ser números!");
      } else {
        insertList(inputFonte, inputPh, inputHard, inputSolid, inputChlo, inputCondc, inputSulf, inputOrgn, inputTrih, inputTurb);
        postItem(inputFonte, inputPh, inputHard, inputSolid, inputChlo, inputCondc, inputSulf, inputOrgn, inputTrih, inputTurb);
        alert("Item adicionado!");
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (nome, ph, hard, solid, chlo, sulf, conduc, organCar, trih, turn, potability) => {
  var item = [nome, ph, hard, solid, chlo, sulf, conduc, organCar, trih, turn, potability];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);


  document.getElementById("newInput").value = "";
  document.getElementById("newPh").value = "";
  document.getElementById("newHard").value = "";
  document.getElementById("newSolid").value = "";
  document.getElementById("newChlor").value = "";
  document.getElementById("newConduc").value = "";
  document.getElementById("newSulf").value = "";
  document.getElementById("newOrgan").value = "";
  document.getElementById("newTrih").value = "";
  document.getElementById("newTurb").value = "";

  removeElement();
}