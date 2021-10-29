const d=document;
const pass = document.querySelector(".js-pass"),
    repass = document.querySelector(".js-repass");
contactFormValidations();
var $select = document.querySelector(".js-pais");
var $flag = document.querySelector(".js-flag");
$select.addEventListener('input', e => {
  var id = e.target.value;
  id = id.toLowerCase()
  $flag.src= `https://flagcdn.com/w40/${id}.png` ;
});

function contactFormValidations(){
  const form = document.querySelector(".js-register-form"),
  inputs = document.querySelectorAll(".js-register-form [required]");
  inputs.forEach(input =>{
    const span=d.createElement('span');
    span.id = input.name;
    span.textContent = input.title;
    span.classList.add("alert", "alert-danger", "d-none")
    input.insertAdjacentElement("afterend", span);
  });

  document.addEventListener('keyup', (event) => {
    if(event.target.matches(".js-register-form [required]")){
      let $input = event.target,
        pattern = $input.pattern || $input.dataset.pattern;
        pass1 = pass.value;
        pass2 = repass.value
    if (pattern && $input.value != ""){
      let regEx = new RegExp(pattern);
      return !regEx.exec($input.value) ? d.getElementById($input.name).classList.add("is-active") : d.getElementById($input.name).classList.remove("is-active");
      }

    if (!pattern){
      if ($input.name == 'Rpassword'){
        verificarPasswords();
      }
      return ($input.value === "")?
      d.getElementById($input.name).classList.add("is-active"):
      d.getElementById($input.name).classList.remove("is-active");
    }
  }
  });
}
d.addEventListener('submit', (event) =>{
  event.preventDefault();
  alerts = document.querySelectorAll(".alert.is-active")
  if (alerts.length == 0){
    event.target.submit();
  }
  else{
    alert("error al enviando formulario");
  }
});

function verificarPasswords() {
  var x = document.getElementById("Rpassword");
  // Ontenemos los valores de los campos de contraseñas 
  var pass1 = document.getElementById('pass'),
  pass2 = document.getElementById('Rpass');

  // Verificamos si las constraseñas no coinciden 
  if (pass1.value != pass2.value) {
      // Si las constraseñas no coinciden mostramos un mensaje 
      console.log(x.classList)
      x.classList.remove("d-none");
      return false 
    } else {
      x.classList.add("d-none")
  }

}
