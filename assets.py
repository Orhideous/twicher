from flask.ext.assets import Bundle

bundles = {
    'vendor_js': Bundle(
        'vendor/js/bootstrap.min.js',
        'vendor/js/jquery-2.1.3.min.js',
        output='dist/js/vendor.js'
    ),
    'vendor_css': Bundle(
        'vendor/css/bootstrap.min.css',
        output='dist/css/vendor.css'
    ),
}
