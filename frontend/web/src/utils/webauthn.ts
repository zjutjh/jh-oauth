export default class WebAuthn {
  public Host: string = 'localhost';
  public HostName: string = 'localhost';



  constructor(domin: string = 'localhost', dominName: string = 'localhost') {
    this.Host = domin;
    this.HostName = dominName;
  }

  public async SignUp(ServerChallenge: string, User: PublicKeyCredentialUserEntity, Timeout: number) {
    const publicKeyCredentialCreationOptions: PublicKeyCredentialCreationOptions = {
      challenge: Uint8Array.from(ServerChallenge, (c) => c.charCodeAt(0)),
      rp: {
        name: this.HostName,
        id: this.Host,
      },
      user: User,
      authenticatorSelection: {
        requireResidentKey: false,
        userVerification: 'discouraged',
      },
      pubKeyCredParams: [
        { alg: -7, type: 'public-key' },
        { alg: -35, type: 'public-key' },
        { alg: -36, type: 'public-key' },
        { alg: -257, type: 'public-key' },
        { alg: -258, type: 'public-key' },
        { alg: -259, type: 'public-key' },
        { alg: -37, type: 'public-key' },
        { alg: -38, type: 'public-key' },
        { alg: -39, type: 'public-key' },
        { alg: -8, type: 'public-key' },
      ],
      timeout: Timeout,
      attestation: 'none',
    };
    const credential = await navigator.credentials.create({
      publicKey: publicKeyCredentialCreationOptions,
    });

    return credential;
  }

  public async Authn(ServerChallenge: string, credentialId: string) {
    const publicKeyCredentialRequestOptions: PublicKeyCredentialRequestOptions = {
      challenge: Uint8Array.from(ServerChallenge, (c) => c.charCodeAt(0)),
      allowCredentials: [{
        id: Uint8Array.from(credentialId, (c) => c.charCodeAt(0)),
        type: 'public-key',
      }],
      timeout: 60000,
    };

    const assertion = await navigator.credentials.get({
      publicKey: publicKeyCredentialRequestOptions,
    });
    return assertion;
  }
}
