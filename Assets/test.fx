{
  "Emitters": [
    {
      "Name": "Emitter 2",
      "Identifier": "f5167654-4ecb-4e4c-8eb1-6a86e330084d",
      "Enabled": true,
      "MaxParticles": 1000,
      "Delay": 0,
      "Duration": 0,
      "PreWarm": 0,
      "TimeScale": 1,
      "Timing": "GameTime",
      "SpawnModules": [
        {
          "__type": "Rinten.SpawnRateModule",
          "Stage": "Spawn",
          "Rate": {
            "UseParameter": false,
            "Value": 10,
            "ParameterName": null,
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "159fc018-d27c-4bfd-b24a-751c4d702861",
          "Name": "Spawn Rate",
          "Enabled": true
        }
      ],
      "InitializeModules": [
        {
          "__type": "Rinten.InitializePositionModule",
          "Stage": "Initialize",
          "Shape": "Sphere",
          "Follows": "Rotation, Scale",
          "Radius": 0.5,
          "BoxSize": "1,1,1",
          "ConeAngle": 45,
          "OnShell": false,
          "LineStart": "0,0,0",
          "LineEnd": "0,1,0",
          "Identifier": "0cda6a44-9ae5-47ee-bc9d-414bbb0fb768",
          "Name": "Position",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeVelocityModule",
          "Stage": "Initialize",
          "Velocity": {
            "UseParameter": true,
            "Value": {
              "X": 0,
              "Y": 2,
              "Z": 0
            },
            "ParameterName": "Vector1",
            "Multiplier": 1,
            "IsBound": true
          },
          "Scatter": {
            "UseParameter": false,
            "Value": 0,
            "ParameterName": null,
            "Multiplier": 1,
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
          "Identifier": "42290eb1-b590-4210-a182-ffd004de4943",
          "Name": "Velocity",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeLifetimeModule",
          "Stage": "Initialize",
          "Lifetime": {
            "UseParameter": false,
            "Value": 2,
            "ParameterName": null,
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "ccc4ca3a-6cd3-4db2-956e-c1656828fd64",
          "Name": "Lifetime",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeSizeModule",
          "Stage": "Initialize",
          "Size": {
            "UseParameter": false,
            "Value": 0.25,
            "ParameterName": null,
            "Multiplier": 1,
            "IsBound": false
          },
          "InheritEmitterScale": true,
          "Identifier": "0d53c4e7-cae8-4100-aeea-c722a3b43e72",
          "Name": "Size",
          "Enabled": true
        },
        {
          "__type": "Rinten.InitializeColorModule",
          "Stage": "Initialize",
          "Color": {
            "UseParameter": false,
            "Value": "1,1,1,1",
            "ParameterName": null,
            "IsBound": false
          },
          "Alpha": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Multiplier": 1,
            "IsBound": false
          },
          "Brightness": {
            "UseParameter": false,
            "Value": 1,
            "ParameterName": null,
            "Multiplier": 1,
            "IsBound": false
          },
          "Tint": "1,1,1,1",
          "Identifier": "8138a78a-d2e9-4110-a163-a99e759f1abc",
          "Name": "Color",
          "Enabled": true
        }
      ],
      "UpdateModules": [
        {
          "__type": "Rinten.GravityModule",
          "Stage": "Update",
          "Force": {
            "UseParameter": false,
            "Value": {
              "X": 0,
              "Y": 0,
              "Z": -9.8
            },
            "ParameterName": null,
            "Multiplier": 1,
            "IsBound": false
          },
          "Identifier": "7c2e8f27-bcd9-4f62-bf86-e576fc5068cc",
          "Name": "Gravity",
          "Enabled": true
        }
      ],
      "RenderModules": [
        {
          "__type": "Rinten.SpriteRenderModule",
          "Stage": "Render",
          "Sprite": null,
          "Scale": 1,
          "Alignment": "Particle",
          "FaceVelocity": false,
          "Additive": false,
          "Shadows": false,
          "Lighting": false,
          "DepthFeather": 0,
          "Identifier": "ac4773f1-fd27-453f-9a51-8670800ceac7",
          "Name": "Sprite",
          "Enabled": true
        }
      ]
    }
  ],
  "Duration": 5,
  "Looping": true,
  "FloatParameters": [
    {
      "DefaultValue": 1,
      "Name": "Float1",
      "Identifier": "15b5ec4b-f1d5-4308-bedd-d9ab9cc72cdc"
    }
  ],
  "VectorParameters": [
    {
      "DefaultValue": "1,1,1",
      "Name": "Vector1",
      "Identifier": "a3bae25e-29a3-44ce-a2c8-7c7044b88c69"
    }
  ],
  "ColorParameters": [],
  "__references": [],
  "__version": 0
}