{ pkgs, ... }:

{
  # ─── Nix channel ──────────────────────────────────────────────────────────
  # "stable-23.11" is the recommended IDX channel for most projects.
  channel = "stable-23.11";

  # ─── System packages ──────────────────────────────────────────────────────
  # Python 3.11 + pip. No Node.js needed: the frontend is plain HTML/JS
  # with no build step — Flask serves the static files directly.
  packages = [
    pkgs.python311
    pkgs.python311Packages.pip
  ];

  # ─── Environment variables ────────────────────────────────────────────────
  # FLASK_ENV controls debug mode. Set to "production" for a quieter log.
  env = {
    FLASK_ENV = "development";
  };

  # ─── IDX-specific configuration ───────────────────────────────────────────
  idx = {

    # VS Code / IDX extensions (add more as needed).
    extensions = [
      "ms-python.python"
    ];

    # ── Lifecycle hooks ──────────────────────────────────────────────────────
    workspace = {

      # onCreate: runs ONCE when the workspace is first created.
      # Use this for one-time setup that should not repeat on every boot.
      onCreate = {
        install-python-deps = "pip install -r requirements.txt";
      };

      # onStart: runs every time the workspace boots.
      # NOTE: Do NOT start the Flask server here — the previews block below
      # handles that exclusively. Running it in both places would cause a
      # "port already in use" crash on boot.
      onStart = {
        # Verify the environment is healthy on each boot (safe read-only check).
        check-env = "python --version && pip show flask | grep Version";
      };
    };

    # ── Preview panel configuration ──────────────────────────────────────────
    # This is the single source of truth for starting the server in IDX.
    # IDX launches the `command` in a managed process, then opens port 5000
    # in the browser preview panel automatically.
    previews = {
      enable = true;
      previews = {
        web = {
          # The exact command that boots the unified Flask server.
          # Flask serves BOTH the REST API (/api/*) and all HTML pages (/).
          command = [ "python" "app.py" ];
          manager = "web";
          port = 5000;
        };
      };
    };

  }; # end idx

}
