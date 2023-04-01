import 'bootstrap'
import './sass/style.scss'

import * as bootstrap from 'bootstrap'

// TODO reduce based on usage
import '@fortawesome/fontawesome-free/scss/fontawesome.scss';
import '@fortawesome/fontawesome-free/scss/brands.scss';
import '@fortawesome/fontawesome-free/scss/regular.scss';
import '@fortawesome/fontawesome-free/scss/solid.scss';

import $ from 'jquery'
import './js/hanusovedni'
import './js/stream'


// This is for events page - to be able to use jQuery before calling Elm
window.$ = $
