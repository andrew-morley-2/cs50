from flask import Flask, render_template, request, flash
from helpers import apology, login_required
import urllib.request
import xmltodict
from flask_dance.contrib.azure import make_azure_blueprint
import ssl
import csv
import json


# Configure application and authentication with Azure AD
app = Flask(__name__)
blueprint = make_azure_blueprint(client_id="###########", client_secret="###########")
app.register_blueprint(blueprint, url_prefix="/")


# Set secret key for sessions
app.secret_key = b'"###########'

# Fix issues with api calls related to certificates
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show homepage upon login"""
    # Sites list/table can alternatively be implemented with Prisma SASE (API) via the following: https://pan.dev/access/docs/insights/examples/remote-networks-dashboard/rn-list/

    # Open sites csv file
    sites_file = open('sites.csv')

    # Set variable for reading csv file
    csvreader = csv.reader(sites_file)

    # Set cursor to next line to skip headers
    next(csvreader)

    # Define empty lists for table use
    tunnel_name = []
    status = []
    palocation = []
    panode = []
    ipsec = []
    compute = []
    aggband = []
    peakband = []
    avgband = []
    tunnelsup = []
    totaltunnels = []

    # Go through csv and append list entries
    for i in csvreader:
        tunnel_name.append([i][0][0])
        status.append([i][0][1])
        palocation.append([i][0][2])
        panode.append([i][0][3])
        ipsec.append([i][0][4])
        compute.append([i][0][5])
        aggband.append([i][0][6])
        peakband.append([i][0][7])
        avgband.append([i][0][8])
        tunnelsup.append([i][0][11])
        totaltunnels.append([i][0][12])

    # Close csv files
    sites_file.close()

    # Send user to GP, send lists to page to be displayed in table
    return render_template("index.html", sites_info=zip(tunnel_name, status, palocation, panode, ipsec, compute, aggband, peakband, avgband, tunnelsup, totaltunnels))

# Return user to home page
if __name__ == "__main__":
    app.run(host='localhost', port=4000)


@app.route("/globalprotect", methods=["GET", "POST"])
@login_required
def globalprotect():
    """Show GlobalProtect Information and Disconnect Users via Button"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Set variable to username entry on GlobalProtect page
        username_entry = request.form.get("username")

        # Ensure username was submitted
        if not username_entry:
            return apology("must provide username", 400)

        # Ensure username is a valid length
        if not len(username_entry) == 6:
            return apology("username length is invalid", 400)

        # Ensure username begins with correct character
        if not username_entry[0] == 'u':
            return apology("username must begin with u", 400)

        # Send XML API GET to Firewall to disconnect user based on the username entry
        f"https://192.168.1.188//api/?type=op&cmd=<request><global-protect-gateway><client-logout><user>{username_entry}</user></client-logout></global-protect-gateway></request>&key###########"

        # Display success message
        flash('Your request was sent successfully')

    # Can alternatively be implemented with Prisma SASE (API) via the following: https://pan.dev/access/docs/insights/examples/mobile-users-dashboard/mu-users-list/

    # Open users csv file
    users_file = open('users.csv')

    # Set variable for reading csv file
    csvreader = csv.reader(users_file)

    # Set cursor to next line to skip headers
    next(csvreader)

    # Define empty lists for table use
    name = []
    location = []
    prismagw = []
    country = []
    privateip = []
    publicip = []
    logintime = []
    clientinfo = []

    # Go through csv and append list entries
    for i in csvreader:
        name.append([i][0][0])
        location.append([i][0][1])
        prismagw.append([i][0][2])
        country.append([i][0][3])
        privateip.append([i][0][4])
        publicip.append([i][0][5])
        logintime.append([i][0][6])
        clientinfo.append([i][0][7])

    # Close csv file
    users_file.close()

    # Send user to GP, send lists to page to be displayed in table
    return render_template("globalprotect.html", users_info=zip(name, location, prismagw, country, privateip, publicip, logintime, clientinfo))


@app.route("/tunnels")
@login_required
def tunnels():
    """Show Tunnel Information"""

    # Define variable for initial tunnel api call to firewall for list of names
    get_tunnels = "https://192.168.1.188//api/?type=op&cmd=<show><vpn><tunnel></tunnel></vpn></show>&key=###########"

    # Take XML response and parse the data
    tunnels_response_object = urllib.request.urlopen(get_tunnels)
    tunnels_data = tunnels_response_object.read()
    tunnels_response_object.close()
    tunnels_data = xmltodict.parse(tunnels_data)

    # Create empty lists for tunnel data
    tunnel_list= []
    tunnel_status= []
    tunnel_encap= []
    tunnel_decap= []

    # Find number of of tunnels
    tunnels_length = len(tunnels_data['response']['result']['entries']['entry'])

    # Loop through tunnel entries and append name. Also do another api call for each tunnel, parse data, and append status
    for i in range(tunnels_length):
        tunnel_list.append(tunnels_data['response']['result']['entries']['entry'][i]['name'])
        get_flow = f"https://192.168.1.188//api/?type=op&cmd=<show><vpn><flow><name>{tunnels_data['response']['result']['entries']['entry'][i]['name']}</name></flow></vpn></show>&key=###########"
        flow_response_object = urllib.request.urlopen(get_flow)
        flow_data = flow_response_object.read()
        flow_response_object.close()
        flow_data = xmltodict.parse(flow_data)
        if flow_data['response']['result'] is None:
            tunnel_status.append("down")
            tunnel_encap.append(" ")
            tunnel_decap.append(" ")
        else:
            tunnel_status.append("up")
            tunnel_encap.append(flow_data['response']['result']['entry']['pkt-encap'])
            tunnel_decap.append(flow_data['response']['result']['entry']['pkt-decap'])


    # Send user to GP
    return render_template("tunnels.html", tunnel_info=zip(tunnel_list, tunnel_status, tunnel_encap, tunnel_decap))


@app.route("/split-tunneling")
@login_required
def split_tunneling():
    """Show Tunnel Information"""

    # Define variable for initial split-tunneling api call to firewall for list of entries
    get_tunneling = "https://192.168.1.188///api/?type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/vsys/entry[@name='vsys1']/global-protect/global-protect-gateway/entry[@name='GP']/remote-user-tunnel-configs/entry[@name='GP']/split-tunneling/exclude-access-route&key=###########"

    # Take XML response and parse the data
    tunneling_response_object = urllib.request.urlopen(get_tunneling)
    tunneling_data = tunneling_response_object.read()
    tunneling_response_object.close()
    tunneling_data = xmltodict.parse(tunneling_data)

    # Create empty list of split-tunneling entries
    tunneling_list= []

    # Find number of split-tunneling entries
    tunneling_length = len(tunneling_data['response']['result']['exclude-access-route']['member'])

    for i in range(tunneling_length):
        tunneling_list.append(tunneling_data['response']['result']['exclude-access-route']['member'][i])

    # Send user to GP
    return render_template("split-tunneling.html", tunneling_info=tunneling_list)

@app.route("/diagram")
@login_required
def diagram():
    """Show diagram"""

    # Send user to diagram page
    return render_template("diagram.html")

@app.route("/egress-ip")
@login_required
def egress_ip():
    """Show all egress IP addresses for SD-WAN and Remote VPN"""

    # Can alternatively be implemented with Prisma SASE (API) via the following: https://docs.paloaltonetworks.com/prisma/prisma-access/prisma-access-panorama-admin/prisma-access-overview/retrieve-ip-addresses-for-prisma-access/

    # Open and read JSON file/data for mobile users/globalprotect
    mu_file = open('mu.json')
    mu_data = json.load(mu_file)

    # Create empty lists to be used in table display
    ip = []
    ip_type = []

    # Loop through mobile user data for addresses and mark them as GlobalProtect
    for i in mu_data["addresses"]:
        ip.append([i][0])
        ip_type.append("GlobalProtect")

    # Open and read JSON file/data
    rn_file = open('rn.json')
    rn_data = json.load(rn_file)

    # Loop through remote network data for addresses and mark them as Remote Network
    for i in rn_data["addresses"]:
        ip.append([i][0])
        ip_type.append("Remote Network")

    # Close files
    mu_file.close()
    rn_file.close()

    # Send user to diagram page
    return render_template("egress-ip.html", egress_info=zip(ip_type, ip))