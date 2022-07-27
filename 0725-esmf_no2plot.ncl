load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRF_contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"

begin

ts = 5   ;起始时间   ncdump查看每天小时数 然后计算自己画图时间段起始序号
te = 5   ;结束时间


	f_no2 = systemfunc("ls " + "/GFPS8p/wuk/bxb/CMAQ/20190*.ncf" )

    print(f_no2(0))  
    day1 = dimsizes(f_no2)
    data_mis = new((/day1,te-ts+1,1,228,198/),"float")
    do dd = 0, day1 - 1
		ff_no2 = addfile(f_no2(dd), "r")
		data_mis(dd,:,:,:,:) = ff_no2->NO2_COLUMN(ts:te,:,:,:)
	end do

    mis_avg = dim_avg_n_Wrap(data_mis, (/0,1/))

;地理信息
    fmapname      = "/GFPS8p/wuk/bxb/GRIDCRO2D_2018365.nc"
    fmap    = addfile(fmapname,"r")

    LatF    = fmap->LAT(0,0,:,:)
    LonF    = fmap->LON(0,0,:,:)


    lat = fspan(27.5,35,800)
    lon = fspan(115,122,800)

;---Set up regridding options
    Opt                   = True

;---"bilinear" is the default. "patch" and "conserve" are other options.
    Opt@InterpMethod      = "bilinear"        ;;---Change (maybe)

    Opt@WgtFileName       = "WRF_to_rect.nc"

    Opt@SrcGridLat        = LatF           ; source grid
    Opt@SrcGridLon        = LonF
    Opt@SrcRegional       = True              ;;--Change (maybe)
;    Opt@SrcInputFileName  = src_file          ; optional, but good idea
    Opt@DstGridType       = "rectilinear"
    Opt@DstGridLat        = lat           ; destination grid
    Opt@DstGridLon        = lon
    Opt@DstRegional       = True              ;;--Change (maybe)

    Opt@ForceOverwrite    = True
    Opt@PrintTimings      = True
    Opt@Debug             = True

    mis_regrid1 = ESMF_regrid(mis_avg,Opt)     ; Do the regridding

    mis_regrid = dim_avg_n_Wrap(mis_regrid1, 0)
    printVarSummary(mis_regrid)


    f2 =  "/GFPS8p/wuk/bxb/txt/201901YRD.txt"

    obs = new((/800,800/),"float")
    obs = asciiread(f2,(/800,800/),"float") 

    lat@units="degrees_north"
    lat@long_name ="latitude"
    lon@units="degrees_east"
    lon@long_name ="longitude"

    obs!0="lat"
    obs!1 ="lon"
    obs&lat = lat
    obs&lon = lon

;mis_obs = obs
    mis_obs = (mis_regrid - obs)

    printMinMax(mis_obs, 0)
    copy_VarCoords(obs, mis_obs)
    printVarSummary(mis_obs)

    fout = addfile("/GFPS8p/wuk/bxb/2019-01-NO2.nc","c")
    fout->s5pNO2     = obs
    fout->CMAQNO2    = mis_regrid
    fout->DIF        = mis_obs

end

