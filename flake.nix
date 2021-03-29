

{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
    #poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.url = "github:sireliah/poetry2nix/mk-poetry-propagate-packages";
  };

  outputs = { self, nixpkgs, poetry2nix, utils }:
    utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; overlays = [ poetry2nix.overlay ]; };
    in rec {
      # `nix build`
      packages.datastuff = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ./.;
      };

      defaultPackage = packages.datastuff;

      # `nix run`
      apps.meupload = utils.lib.mkApp {
        drv = packages.datastuff;
      };
      defaultApp = apps.datastuff;

      # `nix develop`
      devShell = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ./.;
        python = pkgs.python39;
      };

    });
}
