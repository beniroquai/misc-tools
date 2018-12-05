%% Construct Greensfunction
% Need DIPIMAGE Toolbox
% According to https://arxiv.org/abs/1705.04281
nEmbb = 1.33; 
nObj = 1.52;
lambda0 = .6; % measured in µm

Nx = 128;
Ny = Nx;
Nz = Nx;

% proper Sampling?!
pixelsize = lambda/4;
deltaY = pixelsize;
deltaZ = pixelsize;


% Compute wave-number in medium
k0 = 2*pi/lambda0;
kb = 2*pi/lambda0*sqrt(nEmbb);

mysize = [Nx Ny Nz];
kr = (rr(mysize)*(1/(Nx*pixelsize)));

% My approach
GreensFkt = exp((1i*kb)*abs(kr)) ./ abs(4*pi*kr);
GreensFkt(MidPosX(GreensFkt),MidPosY(GreensFkt), MidPosZ(GreensFkt))=1.0/sqrt(2);
GreensFkt_Ft = ft(GreensFkt);

GreensFkt_Ft(:,:,Nz/2)

imshow(abs(double(GreensFkt_Ft(:,:,Nz/2)))), colorbar

% Introduce some sample:
mysphere = rr(mysize)<8;
f_obj = nObj*mysphere;
f = k0^2*(f_obj-nEmbb);

