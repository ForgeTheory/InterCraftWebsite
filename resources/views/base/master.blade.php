<!doctype html>
<html lang="{{ app()->getLocale() }}">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">

        <title>{{ $title }}</title>

        <link href="/css/app.css" rel="stylesheet" type="text/css">
        @stack("head")
    </head>
    <body>
        {{-- Main content --}}
        <header>
            @yield("header")
        </header>
        <div class="container-fluid">
            @yield("body")
        </div>
        <footer>
            @yield("footer")
        </footer>

        {{-- Scripts --}}
        <script src="/js/app.js"></script>
        @stack("scripts")
    </body>
</html>