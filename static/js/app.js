const footer = document.getElementById('toggle')
const body = document.getElementById('body')
const paginator = document.querySelector('.pagination')

if (body.scrollHeight < document.documentElement.scrollHeight) {
    footer.classList.add('fixed-bottom')}
else footer.classList.remove('fixed-bottom')
