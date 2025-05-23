# Changelog

## [1.15.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.14.2...v1.15.0) (2024-07-02)


### Features

* Filter out experiments - processing ([44fcf2c](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/44fcf2c11027edb6ef9bfcfe6e26a2f59a6e9a09))
* make it possible to force paired reads when combining samples and fastq files ([be02866](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/be028665b620b3aacd0a5ef60dac74c2bb2e7baa))


### Bug Fixes

* Use path to file instead of string. ([4d1ddb5](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/4d1ddb585792a173d2e4fe93b983816c90552ea3))

### [1.14.2](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.14.1...v1.14.2) (2024-06-17)


### Bug Fixes

* set timeout to 0 which is equal to no timeout ([95b4a4d](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/95b4a4daf0e0673944fa93ca836444a20dc1c09e))

### [1.14.1](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.14.0...v1.14.1) (2024-06-14)


### Bug Fixes

* handle gms560 with stuff in description ([6861e98](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/6861e9836ec9a3d44b68c1c18ca1841d65cb888b))

## [1.14.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.13.0...v1.14.0) (2024-05-27)


### Features

* extract type when converting old format to new format ([df9682c](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/df9682ca4b781d7324f4e46651d05caf1c7c4b42))


### Bug Fixes

* change match to search ([ad9205c](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/ad9205cd4d5ae7b72cf68ac2a615cb2fc3293d62))
* handle sample_project ([76d48dd](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/76d48dd6d17c57bc2f95ee19f565188b4d960a47))

## [1.13.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.12.0...v1.13.0) (2024-05-24)


### Features

* change method name from sera to haloplex-idt ([5852231](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/5852231de132905144ac3bbb28378c0cc2b22ad0))

## [1.12.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.11.3...v1.12.0) (2024-05-14)


### Features

* setup executable script (rsync.py) ([91a95c0](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/91a95c046662762a791ea9c89bfd4df295d0995b))

### [1.11.3](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.11.2...v1.11.3) (2024-05-13)


### Bug Fixes

* handle old project format wp1 ([3b014b3](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/3b014b3dad75893b621b8da047cec135594570c5))
* minor change to make old sera format compatible with new ductus ([efaeec0](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/efaeec03448880f6db819e82a05e94db00953b16))

### [1.11.2](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.11.1...v1.11.2) (2024-05-09)


### Bug Fixes

* add missing library ([9ed96c3](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/9ed96c318a71f809e4e29764ea9a4b175d7ca89f))

### [1.11.1](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.11.0...v1.11.1) (2024-05-09)


### Bug Fixes

* read file from windows with special characters ([6431ea3](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/6431ea3f12afc87762e6b54cea02832af6a80320))

## [1.11.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.10.0...v1.11.0) (2024-05-08)


### Features

* update tc key to tumor_content and add documentation ([b45f152](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/b45f152573aa0e47d97395e708a08b9da205e8ad))


### Bug Fixes

* update wp3 sample sheet key ([40222e0](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/40222e05633ef368d5fa061b98d9f04fcdf20022))

## [1.10.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.9.0...v1.10.0) (2024-02-02)


### Features

* convert sera samplsheet and index file to new analysis file. And fix generate statistics ([7094bef](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/7094befa5d1f7477deea0518b574745915b932e0))


### Bug Fixes

* make compatible with old ductus ([1a64a2b](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/1a64a2b7c8070d1d9f3df86ca6f16e4fe6415ccd))
* make statistics match new format of settings ([c8fb268](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/c8fb26876078125cd22a322b4a0ac09534af60c0))
* remove , from sera index file, replace it with ; ([dd8b4d0](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/dd8b4d0664a14ab76daba7dc08c9a908099f43e3))
* revert change in experiment name detection ([7eaf3d2](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/7eaf3d2b39476e132c206ab41cbcac835ba99ecc))

## [1.9.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.8.0...v1.9.0) (2024-01-18)


### Features

* add functions to match samples with fastq files and to create json update structures ([a183e52](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/a183e5258f96d58a9aacc14ecf7aad45795969ce))
* add wp info to get_experiments dict and update tests ([fb81f5c](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/fb81f5cace035c9fdb2d15e8208518621d5b6984))
* function used to convert between old and new format ([f85b96f](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/f85b96f2f0bd18da1ce69c805876517d88c5a0bf))
* make it possible to detetch if SampleSheet follow CGU new or old format ([14c9e51](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/14c9e51140524601cfebf1ec299a45368659ab51))
* start support new wp1 and analysis format string ([070760e](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/070760e62000a22907652da5b33a348ee6ccda29))


### Bug Fixes

* change delimeter from _ to - for combined project and sampe name ([1d63984](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/1d63984745e49958be2ec44e9f9e5280d4da45b2))

## [1.8.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.7.0...v1.8.0) (2023-04-21)


### Features

* add abl ([d2d8351](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/d2d8351655a1775ba275c5f4348ce8a107a8bab3))


### Bug Fixes

* **wp1:** allow - in user part of experiment name ([3ae23b9](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/3ae23b930153686cebbca9504ee8bb9edf53a149))

## [1.7.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.6.0...v1.7.0) (2023-01-24)


### Features

* add get_project_and_experiment function ([34a578f](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/34a578fabf782e2f74b61e4b758ce701b89c7e37))
* add test for get_project_and_experiment ([4369e5f](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/4369e5f210b5be78c3dad4fb3e06d7afe0f3a638))

## [1.6.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.5.0...v1.6.0) (2022-12-12)


### Features

* added GMS560 analysis ([fab67ed](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/fab67ed08c75d9be64ddbceb22faff35f7f66aa9))


### Bug Fixes

* fixed so that tests run ok ([06f6bd6](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/06f6bd66e8c51ed64bb22921eb71700260c94095))

## [1.5.0](https://www.github.com/clinical-genomics-uppsala/ductus-core/compare/v1.4.0...v1.5.0) (2022-02-18)


### Features

* add check for semantic commits ([6d4fa2e](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/6d4fa2e66df94532b1c4857e6951151b75f1e174))
* add release-please workflow ([e78207a](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/e78207a9a90a70b651f567ce0b13ae8038a20658))
* get version using versioneer ([9bd442b](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/9bd442baaa260a62aaf54cc8232df615c0d2d492))


### Bug Fixes

* handle case where description is missing ([d141aa3](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/d141aa3628804a40518be192d78275deb0194c2c))
* handle case with - in initials ([e206fbd](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/e206fbd0e22f784e54dfe44402e33df16eaf161c))
* handle date with missing leading zeros ([62fb0ff](https://www.github.com/clinical-genomics-uppsala/ductus-core/commit/62fb0ff04bd9297862856204483a047a28549480))
