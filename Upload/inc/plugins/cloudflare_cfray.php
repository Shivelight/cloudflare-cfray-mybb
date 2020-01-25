<?php

// Disallow direct access to this file for security reasons
if (!defined("IN_MYBB")) {
    die("Direct initialization of this file is not allowed.");
}

$plugins->add_hook("global_start", "cloudflare_cfray_resolve");

function cloudflare_cfray_info()
{
    return array(
        "name"          => "Cloudflare CF-Ray",
        "description"   => "Resolve Cloudflare CF-Ray header to human readable location.",
        "website"       => "https://github.com/Shivelight/cloudflare-cfray-mybb",
        "author"        => "Shivelight",
        "authorsite"    => "https://shivelight.id",
        "version"       => "0.1.0",
        "codename"      => "cloudflare_cfray",
        "compatibility" => "18*"
    );
}

function cloudflare_cfray_resolve()
{
    global $cfray;

    if (isset($_SERVER["HTTP_CF_RAY"])) {
        $cfray_iata = explode("-", $_SERVER["HTTP_CF_RAY"])[1];
        require_once MYBB_ROOT."inc/plugins/cloudflare-cfray/cfray_data.php";
        if (isset($cfray_data[$cfray_iata])) {
            $cfray = $cfray_data[$cfray_iata];
            return;
        }
    }

    // Default, Unknown
    $cfray = array(
        "iata" => "Unknown",
        "city" => "Unknown",
        "state" => "Unknown",
        "country" => "Unknown",
        "alpha2" => "XX",
    );
}
