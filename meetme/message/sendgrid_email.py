import logging
import sendgrid
import meetme.settings
import meetme.server.render


def send_sync(to=None, from_address='noreply@meetme.com', subject=None, text_template=None, html_template=None, **kwargs):
  if meetme.settings.DEBUG:
    logging.debug('pretending to send an email to: %s' % to)
    return
  if meetme.settings.ENVIRONMENT == 'staging':
    logging.debug('pretending to send an email to: %s' % to)
    return


  text = meetme.server.render.render_template(text_template, **kwargs)
  html = meetme.server.render.render_template(html_template, **kwargs)

  sg = sendgrid.SendGridClient(meetme.settings.SENDGRID_USERNAME, meetme.settings.SENDGRID_PASSWORD, secure=True)
  message = sendgrid.Mail()

  message.add_to(to)
  message.set_subject(subject)
  message.set_text(text)
  message.set_html(html)
  message.set_from(from_address)
  message.set_from_name('meetme')
  status, msg = sg.send(message)
  logging.debug('msg: %s, status: %s' % (msg, status))