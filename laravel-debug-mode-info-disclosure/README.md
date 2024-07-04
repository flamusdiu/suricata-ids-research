# Suricata Flowbits Test with Lavarel Debug Vuln

Flowbits provides a method to flag matched traffic during host communications. See [Suricata Documentation on Flowbits](https://docs.suricata.io/en/suricata-6.0.19/rules/flow-keywords.html).

For this example, let using Proofpoint's [2034508 - ET SCAN Laravel Debug Mode Information Disclosure Probe Inbound](https://threatintel.proofpoint.com/sid/2034508) rule. Scanning rules will cause a tons of alerts when monitoring external interface. So, flowbits can be added on important rules.

## Steps

### 1. Python Web Server

This uses the [Bottle Web Framework](https://bottlepy.org/docs/dev/).

Start the web server ([server.py](server.py)) from the internal network. You may need to forward ports from a firewall and needs to be with administrator privileges.

Run as:

```shell
python server.py
```

### 2. Run Curl from Remote Computer

Update the command to the proper external IP address.

```shell
curl -XPOST -d "0x%5B%5D=androxgh0st" -A 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36' http://<external_ip>/upload?f=.env
```

## Suricata

### Rules

```shell
alert http any any -> [$HOME_NET,$HTTP_SERVERS] any (msg:"ET SCAN Laravel Debug Mode Information Disclosure Probe Inbound"; flow:established,to_server; http.method; content:"POST"; http.request_body; content:"0x%5B%5D=androxgh0st"; nocase; fast_pattern; flowbits: set, AZ.LaravelScan; flowbits: noalert; reference:url,thedfirreport.com/2021/02/28/laravel-debug-leaking-secrets/; classtype:attempted-recon; sid:2034508; rev:1; metadata:created_at 2021_11_18, updated_at 2021_11_18;)

alert http [$HOME_NET,$HTTP_SERVERS] any -> any any (msg:"AZ EXPLOIT Laravel Debug Mode Information Disclosure Probe Outbound";  flow:established, to_client; http.response_body; content: "APP_KEY="; flowbits: isset, AZ.LaravelScan; sid:1000000;)
```

### Alerts

```text
07/03/2024-13:51:14.061765  [**] [1:1000000:0] AZ EXPLOIT Laravel Debug Mode Information Disclosure Probe Outbound [**] [Classification: (null)] [Priority: 3] {TCP} 172.16.10.117:80 -> 54.245.47.37:47106
```

## Dalton

If you capture a PCAP, you can use [Dalton](https://github.com/secureworks/dalton) to verify the rules instead of setting up a complete sensor.