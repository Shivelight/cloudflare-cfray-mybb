# MyBB Cloudflare CF-Ray

A plugin for MyBB 1.8.x to resolve Cloudflare CF-Ray header IATA code into more human location.

## Installation

1. Upload the contents of the `Upload/` directory to your MyBB root.
2. Activate the plugin from ACP.

## Usage

You can use a variable called `$cfray` in your templates:

```php
$cfray = array(
    "iata" => "CGK",
    "city" => "Jakarta",
    "state" => "",
    "country" => "Indonesia",
    "alpha2" => "ID",
);
```

Example:

```html
<span style="font-family:monospace">Connected via {$cfray['city']}, {$cfray['alpha2']}</span>
```

The result:

```
Connected via Jakarta, ID
```

## Building

To build/update the CF-Ray data (`inc/plugins/cloudflare-cfray/cfray_data.php`), you can simply run the Python script (Python >= 3.5):

```sh
python build.py
```

## Credits

- [pycountry](https://github.com/flyingcircusio/pycountry) for the ISO3166-1 database.
