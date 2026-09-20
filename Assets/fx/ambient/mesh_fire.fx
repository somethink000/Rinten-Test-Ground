{
  "Emitters": [
    {
      "Name": "Flame",
      "Identifier": "90b71cdf-2530-52bb-a554-0aa46cea2d60",
      "Enabled": true,
      "MaxParticles": 4,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0.0,
      "Duration": 0.0,
      "PreWarm": 0.0,
      "TimeScale": 1,
      "Timing": "GameTime",
      "SpawnModules": [
        {
          "__type": "Rinten.SpawnBurstModule",
          "Stage": "Spawn",
          "Count": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "3252d2d0-becf-5093-a85c-57b0bab083b7",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Point",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "51c956af-d2db-5625-88e1-df1b44dba19d",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 4.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "31d0ed83-986f-50e9-afd8-a9886729c0d5",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 1.0,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "074bcc73-4e5a-5fb2-875a-a354245df23a",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": true,
            "Value": "1,1,1,1",
            "ParameterName": "Tint",
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "d3648f38-6d2b-58d5-9088-b94b4668f531",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/fx/flame.mdl",
          "Material": "materials/fx/stylized_fire.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": true,
          "CastShadows": false,
          "PartFromParticle": false,
          "Morphs": [
            {
              "Enabled": true,
              "Name": "Lean",
              "Weight": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.16666666666666666,
                      "y": 0.7,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.3333333333333333,
                      "y": 0.2,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.5,
                      "y": 0.9,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6666666666666666,
                      "y": 0.4,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8333333333333334,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.16666666666666666,
                      "y": 0.7,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.3333333333333333,
                      "y": 0.2,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.5,
                      "y": 0.9,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6666666666666666,
                      "y": 0.4,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8333333333333334,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Sway",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            },
            {
              "Enabled": true,
              "Name": "Flicker",
              "Weight": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.16666666666666666,
                      "y": 0.9,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.3333333333333333,
                      "y": 0.2,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.5,
                      "y": 0.7,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6666666666666666,
                      "y": 1.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8333333333333334,
                      "y": 0.4,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.16666666666666666,
                      "y": 0.9,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.3333333333333333,
                      "y": 0.2,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.5,
                      "y": 0.7,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6666666666666666,
                      "y": 1.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8333333333333334,
                      "y": 0.4,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Flicker",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            },
            {
              "Enabled": true,
              "Name": "Bulge",
              "Weight": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.2,
                      "y": 0.5,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6,
                      "y": 0.6,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.2,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.2,
                      "y": 0.5,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6,
                      "y": 0.6,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.2,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Flicker",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            }
          ],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.25,
                      "y": 0.42,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.5,
                      "y": 0.28,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.75,
                      "y": 0.45,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.25,
                      "y": 0.42,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.5,
                      "y": 0.28,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.75,
                      "y": 0.45,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Burn",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Edge",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.1,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 1.3,
                "ParameterName": "Intensity",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Scroll",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 1.3,
                "ParameterName": "Speed",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Fresnel",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.0,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "64f485f6-ca82-5e69-a102-2f996a0017c1",
          "Name": "Mesh",
          "Enabled": true
        },
        {
          "__type": "Rinten.LightRenderModule",
          "Stage": "Render",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.6039,0.2510,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": true,
            "Value": 8,
            "ParameterName": "Glow",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Radius": {
            "UseParameter": false,
            "Value": 4,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Attenuation": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "MaxLights": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Ratio": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "UseParticleColor": false,
          "CastShadows": false,
          "Identifier": "a625bcb0-9c35-52ed-8a7b-8055b2c7f07a",
          "Name": "Light",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Inner",
      "Identifier": "78b84cfc-f681-5bf6-bfc9-96fafd071256",
      "Enabled": true,
      "MaxParticles": 4,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0.0,
      "Duration": 0.0,
      "PreWarm": 0.0,
      "TimeScale": 1,
      "Timing": "GameTime",
      "SpawnModules": [
        {
          "__type": "Rinten.SpawnBurstModule",
          "Stage": "Spawn",
          "Count": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "5cae734b-34a8-500f-b4aa-77032c90de3b",
          "Name": "Spawn Burst",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Point",
          "Offset": "0,0.05,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "725656d6-8834-5c2b-8665-9bc9ba6d37cd",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 4.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "d62d8390-0a97-5c7f-9fe3-0bbe53c2e662",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": true,
            "Value": 0.55,
            "ParameterName": "Size",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "6bf7edc0-a38a-566a-8413-ae449b719b35",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.9569,0.8157,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "68e87c77-e18b-5f7b-b62d-4ba0f81b575f",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [],
      "RenderModules": [
        {
          "__type": "Rinten.MeshRenderModule",
          "Stage": "Render",
          "Model": "models/fx/flame.mdl",
          "Material": "materials/fx/stylized_fire.mat",
          "Scale": {
            "UseParameter": false,
            "Value": 1.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "RotateWithObject": true,
          "CastShadows": false,
          "PartFromParticle": false,
          "Morphs": [
            {
              "Enabled": true,
              "Name": "Flicker",
              "Weight": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.2,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 1.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6,
                      "y": 0.5,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.9,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.2,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 1.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6,
                      "y": 0.5,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.9,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.8,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Flicker",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            },
            {
              "Enabled": true,
              "Name": "Lean",
              "Weight": {
                "UseParameter": true,
                "Value": {
                  "Type": "Curve",
                  "Evaluation": "Life",
                  "CurveA": [
                    {
                      "x": 0.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.2,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6,
                      "y": 0.4,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ],
                  "CurveB": [
                    {
                      "x": 0.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.2,
                      "y": 0.3,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.4,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.6,
                      "y": 0.4,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 0.8,
                      "y": 0.1,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    },
                    {
                      "x": 1.0,
                      "y": 0.0,
                      "in": 0,
                      "out": 0,
                      "mode": "Flat"
                    }
                  ]
                },
                "ParameterName": "Sway",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              }
            }
          ],
          "Shader": [
            {
              "Enabled": true,
              "Name": "Dissolve",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 0.45,
                "ParameterName": "Burn",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Edge",
              "Width": 1,
              "Value": {
                "UseParameter": false,
                "Value": 0.15,
                "ParameterName": null,
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Emission",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 1.8,
                "ParameterName": "Intensity",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            },
            {
              "Enabled": true,
              "Name": "Scroll",
              "Width": 1,
              "Value": {
                "UseParameter": true,
                "Value": 2.0,
                "ParameterName": "Speed",
                "Mode": "Multiply",
                "Multiplier": 1.0,
                "IsBound": false
              },
              "Color": {
                "UseParameter": false,
                "Value": "1,1,1,1",
                "ParameterName": null,
                "IsBound": false
              },
              "AsVector": false,
              "Vector": {
                "UseParameter": false,
                "Value": {
                  "X": 0.0,
                  "Y": 0.0,
                  "Z": 0.0
                },
                "ParameterName": null,
                "Multiplier": 1.0,
                "ScaleParameterName": null,
                "IsBound": false
              },
              "Min": 0,
              "Max": 1
            }
          ],
          "ParticleAttributes": true,
          "Identifier": "e1ce0715-6c2d-5270-ad4d-414264b631ac",
          "Name": "Mesh",
          "Enabled": true
        }
      ]
    },
    {
      "Name": "Embers",
      "Identifier": "da1be6c0-570a-5a10-8478-407394c7d41f",
      "Enabled": true,
      "MaxParticles": 60,
      "Places": 0,
      "Offset": "0,0,0",
      "Rotation": "0,0,0",
      "Scale": "1,1,1",
      "Anchor": null,
      "Delay": 0.0,
      "Duration": 0.0,
      "PreWarm": 0.0,
      "TimeScale": 1,
      "Timing": "GameTime",
      "SpawnModules": [
        {
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": true,
            "Value": 10,
            "ParameterName": "Embers",
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "bb53bb9e-e1b0-5d97-a4a7-efcde611a55f",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Circle",
          "Offset": "0,0,0",
          "Follows": "Rotation, Scale",
          "Radius": 0.2,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "333bdcef-a197-59a2-845a-c74a4bc3a3f0",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": false,
            "Value": {
              "X": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-0.3,0.3,0,0"
              },
              "Y": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "1.5,2.5,0,0"
              },
              "Z": {
                "Type": "Range",
                "Evaluation": "Seed",
                "Constants": "-0.3,0.3,0,0"
              }
            },
            "ParameterName": null,
            "Multiplier": 1.0,
            "ScaleParameterName": null,
            "IsBound": false
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 0.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "LocalSpace": false,
          "InheritEmitterVelocity": false,
          "InheritScale": 1,
          "Drift": {
            "X": 0,
            "Y": 0,
            "Z": 0
          },
          "Identifier": "f4622a9e-0d5f-5c33-961c-df3c25c3eebd",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "1.2,2.4,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "fefe7b9f-dd2c-548b-b738-9f1c9023ddc7",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": {
              "Type": "Range",
              "Evaluation": "Seed",
              "Constants": "0.02,0.04,0,0"
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "e65e8bd3-b84d-54fa-80bd-41575677e582",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1.0000,0.7529,0.4392,1.0",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": {
              "Type": "Curve",
              "Evaluation": "Life",
              "CurveA": [
                {
                  "x": 0,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.7,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ],
              "CurveB": [
                {
                  "x": 0,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 0.7,
                  "y": 1.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                },
                {
                  "x": 1,
                  "y": 0.0,
                  "in": 0,
                  "out": 0,
                  "mode": "Flat"
                }
              ]
            },
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1.5,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "deb4696a-f440-52b3-a095-0d30c2345050",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.CurlNoiseModule",
          "Stage": "Update",
          "Strength": {
            "UseParameter": false,
            "Value": 1.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Scale": {
            "UseParameter": false,
            "Value": 1.2,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "TimeScale": {
            "UseParameter": false,
            "Value": 2.0,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Offset": "0,0,0",
          "Identifier": "e9c6e0aa-10eb-5efc-9630-41b482f278b5",
          "Name": "Curl Noise",
          "Enabled": true
        },
        {
          "__type": "Rinten.DragModule",
          "Stage": "Update",
          "Damping": {
            "UseParameter": false,
            "Value": 0.3,
            "ParameterName": null,
            "Mode": "Multiply",
            "Multiplier": 1.0,
            "IsBound": false
          },
          "Identifier": "a5f0cbc5-6a3b-54b8-be88-50f89cb560e3",
          "Name": "Drag",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": "sprites/spark.sprite",
          "Scale": 1.0,
          "Alignment": "LookAtCamera",
          "FaceVelocity": true,
          "Additive": true,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "SortMode": "Unsorted",
          "Opaque": false,
          "FogStrength": 1.0,
          "TextureFilter": "Bilinear",
          "MotionBlur": false,
          "LeadingTrail": true,
          "BlurAmount": 0.5,
          "BlurSpacing": 0.5,
          "BlurOpacity": 0.5,
          "Identifier": "45d28a84-efa9-59a4-9f46-d2fd24393a7d",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 4.0,
  "Looping": true,
  "Shapes": [],
  "Slots": [],
  "Anchors": [],
  "FloatParameters": [
    {
      "Name": "Intensity",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "ff7f7d2f-2f2e-5b9a-ac9f-61907d602d66"
    },
    {
      "Name": "Flicker",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "377d3765-1aa5-55ac-93ff-9d68389af1b6"
    },
    {
      "Name": "Sway",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 2,
      "Identifier": "2bae1548-95e9-507b-ad72-a9b3a1d37c36"
    },
    {
      "Name": "Burn",
      "DefaultValue": 1,
      "Min": 0,
      "Max": 3,
      "Identifier": "2c425cda-8c31-5dd2-8f59-ec4dc0714955"
    },
    {
      "Name": "Speed",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "c5652ff3-2ee3-566a-8605-b1bee9390b2f"
    },
    {
      "Name": "Size",
      "DefaultValue": 1,
      "Min": 0.2,
      "Max": 3,
      "Identifier": "aa28643f-24dc-5d1d-8f12-1fa1d19f187c"
    },
    {
      "Name": "Embers",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "d54c5562-fd02-5a46-823c-f0e8e6ece42f"
    },
    {
      "Name": "Glow",
      "DefaultValue": 1.0,
      "Min": 0.0,
      "Max": 3.0,
      "Identifier": "6e941755-ba13-5f6b-b668-a3913c5a96a2"
    }
  ],
  "VectorParameters": [],
  "ColorParameters": [
    {
      "Name": "Tint",
      "DefaultValue": "1.0000,1.0000,1.0000,1.0",
      "Identifier": "a1fadc9b-8b11-5fbe-b23f-ac734be678a7"
    }
  ],
  "__references": [],
  "__version": 0
}