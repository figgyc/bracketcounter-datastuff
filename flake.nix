

{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }:
    utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages."${system}";
    in rec {
      # `nix build`
      packages.beepd = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ./.;
      };

      defaultPackage = packages.beepd;

      # `nix run`
      apps.meupload = utils.lib.mkApp {
        drv = packages.beepd;
      };
      defaultApp = apps.beepd;

      nixosModules.beepd = { config }: let format = pkgs.formats.toml; in {
        options.services.beepd = with nixpkgs.lib.types; {

          enable = mkEnableOption "Beepd automation server.";
          settings = lib.mkOption {
            type = format.type;
            default = {};
          };
          port = lib.mkOption {
            type = int;
            default = 4000;
          };
        };

        config = let cfg = config.services.meupload; in
          nixpkgs.lib.mkIf cfg.enable {
          users.users.beepd = {
            group = config.users.users.beepd.group;
            isSystemUser = true;
          };
          users.groups.beepd = { };

          environment.etc.beepd.source = format.generate "config.toml" config.settings;

          systemd.services.beepd = {
            after = [ "network.target" ];
            path = with pkgs; [ openssl ];
            serviceConfig = {
              User = config.users.users.beepd.name;
              Group = config.users.users.beepd.group;
              ExecStart = "${packages.beepd}/bin/gunicorn -b localhost:${cfg.port} beepd:app";
              WorkingDirectory = "/etc/beepd";
              LimitNOFILE = "1048576";
              LimitNPROC = "64";
              PrivateTmp = "true";
              PrivateDevices = "true";
              ProtectHome = "true";
              ProtectSystem = "strict";
              AmbientCapabilities = "CAP_NET_BIND_SERVICE";
              StateDirectory = "beepd";
            };
            wantedBy = [ "multi-user.target" ];
          };
        };
      };

      # `nix develop`
      devShell = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ./.;
      };

    });
}
