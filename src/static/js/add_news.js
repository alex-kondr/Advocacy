const form = document.forms[0]
access_token = localStorage.getItem("access_token")

form.addEventListener('submit', async event => {
  event.preventDefault()
  message.innerHTML = "Додаю..."

  setTimeout(() => { window.location = `../news?token=${access_token}`; }, 4000);

})


