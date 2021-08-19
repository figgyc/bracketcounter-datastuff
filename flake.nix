{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };

  outputs = { self, nixpkgs, poetry2nix, utils }:
    utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; overlays = [ poetry2nix.overlay ]; };
      appEnv = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ./.;
        python = pkgs.python39;
        overrides = pkgs.poetry2nix.overrides.withDefaults (
          self: super: {
            matplotlib = pkgs.python39Packages.matplotlib;
            setuptools-scm = pkgs.python39Packages.setuptools-scm;
            numpy = pkgs.python39Packages.numpy;
            certifi = pkgs.python39Packages.certifi;
          }
        );
      };
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
      devShell = pkgs.mkShell {
        buildInputs = [
          appEnv
          pkgs.python39Packages.pygobject3
          pkgs.python39Packages.cairocffi
        ];
      };
    });
}
