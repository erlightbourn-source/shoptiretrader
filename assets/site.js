/* TIRE TRADER — founding-seller / launch waitlist capture.
   Static pre-launch shell. Signups POST a best-effort FormSubmit note to Evan's
   Gmail so we're building the seller list before the marketplace goes live. */
(function () {
  "use strict";

  /* FormSubmit random-string alias — routes to Evan's Gmail; brand is
     disambiguated by the _subject line. */
  var FORM_ENDPOINT = "https://formsubmit.co/ajax/d32e4dad5c35cab7cb74c858a6943793";

  function sendForm(payload) {
    return fetch(FORM_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload)
    }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    }).then(function (json) {
      var ok = json && (json.success === true || json.success === "true");
      if (!ok) throw new Error("FormSubmit rejected");
      return json;
    });
  }

  document.querySelectorAll("form[data-capture]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = form.querySelector(".form-success");
      var email = form.querySelector('input[type="email"]');
      var btn = form.querySelector('button[type="submit"]');
      // Honeypot: bots fill the hidden field -> fake success, send nothing.
      var honeypot = form.querySelector('input[name="company"]');
      if (honeypot && honeypot.value) {
        if (note) note.textContent = "You're on the list — we'll be in touch.";
        form.reset();
        return;
      }
      if (email && !email.checkValidity()) { email.reportValidity(); return; }
      if (btn) btn.disabled = true;
      if (note) note.textContent = "Adding you to the founding-seller list…";

      var payload = {
        email: email.value,
        _subject: "Tire Trader — founding seller waitlist (" + (form.dataset.source || "site") + ")",
        _template: "table"
      };

      sendForm(payload).then(function () {
        if (note) note.textContent = "You're in. We'll email you the moment listings open in South Florida — with your Founding Seller status locked in.";
        form.reset();
      }).catch(function () {
        if (note) note.textContent = "Something went wrong — please try again in a moment.";
      }).finally(function () {
        if (btn) btn.disabled = false;
      });
    });
  });
})();
