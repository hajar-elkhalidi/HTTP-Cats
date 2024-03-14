import os
import requests as r
from telegram import Update
from telegram.ext import ContextTypes
from get_http_cats import download_picture

TOKEN = os.environ.get('TOKEN')
BOT_USERNAME = os.environ.get('BOT_USERNAME')

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.message.chat.id

    message_type = update.message.chat.type
    text = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            handle_response(new_text)
        else:
            return
    else:
        handle_response(text)

def handle_response(text: str):
    processed = text.strip().lower()
    valid_status_codes = [
        "100", "101", "102", "103",
        "200", "201", "202", "203", "204", "205", "206", "207", "208", "226",
        "300", "301", "302", "303", "304", "305", "306", "307", "308",
        "400", "401", "402", "403", "404", "405", "406", "407", "408", "409",
        "410", "411", "412", "413", "414", "415", "416", "417", "418", "421",
        "422", "423", "424", "425", "426", "428", "429", "431", "451",
        "500", "501", "502", "503", "504", "505", "506", "507", "508", "510", "511"
    ] 

    if not processed.isdigit() or processed not in valid_status_codes:
        error_message = 'Invalid input! Please provide a valid HTTP status code. 👾'
        print(f'Bot sent an error message: {error_message}')
        r.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={error_message}')
    else:
        status = download_picture(processed)
        caption = get_caption(processed)
        response = r.post(f'https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={chat_id}&caption={caption}',
                        files={'photo': open(status, 'rb')})

        if response.status_code == 200:
            print(f"Bot sent the photo {status} successfully")
        else:
            error_message = f"Failed to send photo. Status code: {response.status_code}"
            print(f'Bot sent an error message: {error_message}')



def get_caption(status_code: str) -> str:
    captions = {
        "100": "This interim response indicates that the client should continue the request or ignore the response if the request is already finished.",
        "101": "This code is sent in response to an Upgrade request header from the client and indicates the protocol the server is switching to.",
        "102": "This code indicates that the server has received and is processing the request, but no response is available yet.",
        "103": "This status code is primarily intended to be used with the Link header, letting the user agent start preloading resources while the server prepares a response or preconnect to an origin from which the page will need resources.",
        "200": 'The request succeeded. The result meaning of "success" depends on the HTTP method:\nGET: The resource has been fetched and transmitted in the message body.\nHEAD: The representation headers are included in the response without any message body.\nPUT or POST: The resource describing the result of the action is transmitted in the message body.\nTRACE: The message body contains the request message as received by the server.',
        "201": 'The request succeeded, and a new resource was created as a result. This is typically the response sent after POST requests, or some PUT requests.',
        "202": 'The request has been received but not yet acted upon. It is noncommittal, since there is no way in HTTP to later send an asynchronous response indicating the outcome of the request. It is intended for cases where another process or server handles the request, or for batch processing.',
        "203": 'This response code means the returned metadata is not exactly the same as is available from the origin server, but is collected from a local or a third-party copy. This is mostly used for mirrors or backups of another resource. Except for that specific case, the 200 OK response is preferred to this status.',
        "204": 'There is no content to send for this request, but the headers may be useful. The user agent may update its cached headers for this resource with the new ones.',
        "205": 'Tells the user agent to reset the document which sent this request.',
        "206": 'This response code is used when the Range header is sent from the client to request only part of a resource.',
        "207": 'Conveys information about multiple resources, for situations where multiple status codes might be appropriate.',
        "208": 'Used inside a <dav:propstat> response element to avoid repeatedly enumerating the internal members of multiple bindings to the same collection.',
        "226": 'The server has fulfilled a GET request for the resource, and the response is a representation of the result of one or more instance-manipulations applied to the current instance.',
        "300": 'The request has more than one possible response. The user agent or user should choose one of them. (There is no standardized way of choosing one of the responses, but HTML links to the possibilities are recommended so the user can pick.)',
        "301": 'The URL of the requested resource has been changed permanently. The new URL is given in the response.',
        "302": 'This response code means that the URI of requested resource has been changed temporarily. Further changes in the URI might be made in the future. Therefore, this same URI should be used by the client in future requests.',
        "303": 'The server sent this response to direct the client to get the requested resource at another URI with a GET request.',
        "304": 'This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.',
        "305": 'Defined in a previous version of the HTTP specification to indicate that a requested response must be accessed by a proxy. It has been deprecated due to security concerns regarding in-band configuration of a proxy.',
        "306": 'This response code is no longer used; it is just reserved. It was used in a previous version of the HTTP/1.1 specification.',
        "307": 'The server sends this response to direct the client to get the requested resource at another URI with the same method that was used in the prior request. This has the same semantics as the 302 Found HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request.',
        "308": 'This means that the resource is now permanently located at another URI, specified by the Location: HTTP Response header. This has the same semantics as the 301 Moved Permanently HTTP response code, with the exception that the user agent must not change the HTTP method used: if a POST was used in the first request, a POST must be used in the second request.',
        "400": 'The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing).',
        "401": 'Although the HTTP standard specifies "unauthorized", semantically this response means "unauthenticated". That is, the client must authenticate itself to get the requested response.',
        "402": 'This response code is reserved for future use. The initial aim for creating this code was using it for digital payment systems, however this status code is used very rarely and no standard convention exists.',
        "403": "The client does not have access rights to the content; that is, it is unauthorized, so the server is refusing to give the requested resource. Unlike 401 Unauthorized, the client's identity is known to the server.",
        "404": "The server cannot find the requested resource. In the browser, this means the URL is not recognized. In an API, this can also mean that the endpoint is valid but the resource itself does not exist. Servers may also send this response instead of 403 Forbidden to hide the existence of a resource from an unauthorized client. This response code is probably the most well known due to its frequent occurrence on the web.",
        "405": 'The request method is known by the server but has been disabled and cannot be used. For example, an API may forbid DELETE-ing a resource.',
        "406": 'This response is sent when the web server, after performing server-driven content negotiation, doesn\'t find any content following the criteria given by the user agent.',
        "407": 'This is similar to 401 but authentication is needed to be done by a proxy.',
        "408": 'This response is sent on an idle connection by some servers, even without any previous request by the client. It means that the server would like to shut down this unused connection. This response is used much more since some browsers, like Chrome, Firefox 27+, or IE9, use HTTP pre-connection mechanisms to speed up surfing.',
        "409": 'This response is sent when a request conflicts with the current state of the server.',
        "410": 'This response is sent when the requested content has been permanently deleted from server, with no forwarding address. Clients are expected to remove their caches and links to the resource. The HTTP specification intends this status code to be used for "limited-time, promotional services". APIs should not feel compelled to indicate resources that have been deleted with this status code.',
        "411": 'Server rejected the request because the Content-Length header field is not defined and the server requires it.',
        "412": 'The client has indicated preconditions in its headers which the server does not meet.',
        "413": 'Request entity is larger than limits defined by server; the server might close the connection or return an Retry-After header field.',
        "414": 'The URI requested by the client is longer than the server is willing to interpret.',
        "415": 'The media format of the requested data is not supported by the server, so the server is rejecting the request.',
        "416": 'The range specified by the Range header field in the request can\'t be fulfilled; it\'s possible that the range is outside the size of the target URI\'s data.',
        "417": 'This response code means the expectation indicated by the Expect request header field can\'t be met by the server.',
        "418": "This code was defined in 1998 as one of the traditional I'm a Teapot responses. It says that the server refuses to brew coffee because it is, permanently, a teapot. This RFC2324 was an April Fools' joke and is not expected to be implemented by actual HTTP servers.",
        "419": 'Reserved for future use. The original intention was that this code might be used as part of some form of digital cash or micropayment scheme, as proposed for example by GNU Taler, but that has not yet happened, and this code is not usually used. Google Developers API uses this status if a particular developer has exceeded the daily limit on requests.',
        "420": 'The HTTP 420 Unknown Error is an error message seen on websites when traffic is on the increase, and the server cannot manage the current volume. It is not a standard response code and is used colloquially to refer to an unknown or uncertain state of affairs.',
        "421": 'The source or destination resource of a method is locked.',
        "422": 'The request was well-formed but was unable to be followed due to semantic errors.',
        "423": 'The resource that is being accessed is locked.',
        "424": 'The request failed due to failure of a previous request.',
        "425": 'Indicates that the server is unwilling to risk processing a request that might be replayed.',
        "426": 'The server refuses to perform the request using the current protocol but might be willing to do so after the client upgrades to a different protocol.',
        "428": 'The origin server requires the request to be conditional.',
        "429": 'The user has sent too many requests in a given amount of time ("rate limiting").',
        "431": 'The server is unwilling to process the request because either an individual header field, or all the header fields collectively, are too large.',
        "444": 'A non-standard status code introduced by nginx for the case when a client closes the connection while nginx is processing the request.',
        "451": 'This status code indicates that the server is denying access to the resource in response to a legal demand.',
        "499": 'This status code is not specified in any RFCs but is used by some HTTP proxies to signal a network read timeout behind the proxy to a client in front of the proxy.',
        "500": 'The server has encountered a situation it doesn\'t know how to handle.',
        "501": 'The request method is not supported by the server and cannot be handled. The only methods that servers are required to support (and therefore that must not return this code) are GET and HEAD.',
        "502": 'This error response means that the server, while working as a gateway to get a response needed to handle the request, got an invalid response.',
        "503": 'The server is not ready to handle the request. Common causes are a server that is down for maintenance or that is overloaded. Note that together with this response, a user-friendly page explaining the problem should be sent.',
        "504": 'This error response is given when the server is acting as a gateway and cannot get a response in time.',
        "505": 'The HTTP version used in the request is not supported by the server.',
        "506": 'The server has an internal configuration error: transparent content negotiation for the request results in a circular reference.',
        "507": 'The server is unable to store the representation needed to complete the request.',
        "508": 'The server detected an infinite loop while processing the request.',
        "510": 'Further extensions to the request are required for the server to fulfill it.',
        "511": 'The 511 status code indicates that the client needs to authenticate to gain network access.',
        "599": 'This status code is not specified in any RFCs, but is used by some HTTP proxies to signal a network connect timeout behind the proxy to a client in front of the proxy.',
    }
    return captions.get(status_code, "No caption available for this status code.")
