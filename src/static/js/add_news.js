const form = document.forms[0]
access_token = localStorage.getItem("access_token")

if (access_token) {
    form.action = `/news/add?token=${access_token}`
}

form.addEventListener('submit', async event => {
  event.preventDefault()
  message.innerHTML = "Додаю..."

  if (access_token) {
    console.log("access")
  }
  window.location = `../news`

})


